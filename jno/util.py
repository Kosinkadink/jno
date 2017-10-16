import os
import re
import shutil
import subprocess
from collections import OrderedDict, namedtuple
from colorama import Fore


# Parameters to be included in .jno
valid_params = {
		'EXEC_DIR',
		'EXEC_LIBS',
		'BOARD',
		'PORT',
		'BAUDRATE',
		'SKETCH_DIR'
	}


# Exception class for jno-related exceptions
class JnoException(Exception):
	pass

# Replaces temporary dictionary values with actual values
def interpret_configs(__location__):
	jno_dict = read_configs(__location__)
	# check if EXEC_DIR exists
	if jno_dict["EXEC_DIR"] in ('NULL','DEFAULT'):
		raise JnoException("EXEC_DIR has not been initialized")
	# perform necessary additions/replacements
	if jno_dict["SKETCH_DIR"] == 'DEFAULT':
		jno_dict["SKETCH_DIR"] = os.getcwd()
	# if not absolute directory, make it local
	elif not jno_dict["SKETCH_DIR"].startswith('/'):
		jno_dict["SKETCH_DIR"] = os.path.join(os.getcwd(),jno_dict["SKETCH_DIR"])
	# create EXEC_LIBS, if DEFAULT
	if jno_dict["EXEC_LIBS"] == 'DEFAULT':
		jno_dict["EXEC_LIBS"] = os.path.join(jno_dict["EXEC_DIR"],'libraries')
	# create EXEC_SCRIPT
	jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["EXEC_DIR"],'arduino')
	# create SKETCH_INO
	jno_dict["SKETCH_INO"] = os.path.join(jno_dict["SKETCH_DIR"],'sketch/sketch.ino')
	# create SKETCH_LIBS
	jno_dict["SKETCH_LIBS"] = os.path.join(jno_dict["SKETCH_DIR"],'lib')

	return jno_dict


# Parses global and local .jno, returning dictionary
def read_configs(__location__):
	jno_dict = {}
	jno_dict = parse_jno_file(jno_dict,__location__)
	if os.path.exists(os.path.join(os.getcwd(),'jno.jno')):
		jno_dict = parse_jno_file(jno_dict,os.getcwd())
	return jno_dict


# Parses .jno file in given directory, returning dictionary
def parse_jno_file(jno_dict,jno_dir):
	new_dict = {}

	with open(os.path.join(jno_dir,'jno.jno'),'rb') as jno:
		for line in jno:
			line = line.strip()
			if len(line) == 0:
				continue
			param,conf_input = line.split('==')
			if param in valid_params:
				new_dict[param] = conf_input

	new_keys = new_dict.keys()
	for key in new_keys:
		if key in jno_dict:
			if new_dict[key] in ('NULL','DEFAULT'):
				continue
		jno_dict[key] = new_dict[key]
	return jno_dict


# Copy and replace all libs from script's lib folder
def move_libs(jno_dict):
	for item in os.listdir(jno_dict["SKETCH_LIBS"]):
		itempath = os.path.join(jno_dict["SKETCH_LIBS"],item)
		if os.path.isdir(itempath):
			execpath = os.path.join(jno_dict["EXEC_LIBS"],item)
			try:
				shutil.copytree(itempath,execpath)
			except OSError:
				shutil.rmtree(execpath)
				shutil.copytree(itempath,execpath)
			finally:
				print(Fore.YELLOW + 'Copied lib {}'.format(item) + Fore.RESET)


# Run arduino with an assembled argument list
def run_arduino_process(arg_list):
	try:
		returned = subprocess.check_call(arg_list)
	except subprocess.CalledProcessError,e:
		returned = e.returncode
	print(Fore.YELLOW + 'All Actions Complete: {}'.format(return_code_qualifier(returned)) + Fore.RESET)


# Returns meaning of return code
def return_code_qualifier(return_code):
	return_code_dict = {
		0:Fore.GREEN + "Success",
		1:Fore.RED + "Build failed or upload failed",
		2:Fore.RED + "Sketch not found",
		3:Fore.RED + "Invalid argument for commandline option",
		4:Fore.RED + "Preference passed to --get-pref does not exist"
	}
	return return_code_dict[return_code]

# Get and print list of all supported models
def get_all_models(jno_dict):
	# directores to ignore
	ignore_dirs = ["tools"]
	# get hardware directory
	arduino_hardware_dir = os.path.join(jno_dict["EXEC_DIR"],"hardware")
	# used to store all models
	all_models = []
	# do a walk
	directories = next(os.walk(arduino_hardware_dir))[1]
	for directory in directories:
		# if not an ignored dir, go into it
		if directory not in ignore_dirs:
			directory_path = os.path.join(arduino_hardware_dir,directory)
			subdirectories = next(os.walk(directory_path))[1]
			# in each directory here, go into it and do a get_boards... call
			for subdir in subdirectories:
				subdir_path = os.path.join(directory_path, subdir)
				path_prefix = "{}:{}:".format(directory,subdir)
				all_models.extend(get_boards_from_directory(subdir_path,path_prefix))
	#arduino_hardware_dir = os.path.join(jno_dict["EXEC_DIR"],"hardware/arduino/avr/")
	return all_models

# Returns model list from boards.txt in specified directory
def get_boards_from_directory_OLD(fileloc):
	# models is a list of tuples
	# [(arduino_label,readable_label,[cpu_type,...]),...]
	models = []
	with open(os.path.join(fileloc,"boards.txt"),'rb') as modelfile:
		current_arduino_label = None
		current_readable_label = None
		current_cpu_types = []
		for line in modelfile:
			if ".name=" in line:
				arduino_label,readable_label = line.strip().split(".name=")
				# check if we are on a different type of board now
				if current_arduino_label is not None and arduino_label != current_arduino_label:
					arduino_model_data = [current_arduino_label,current_readable_label]
					arduino_model_data.append(current_cpu_types)
					models.append(tuple(arduino_model_data))
				# change the current labels
				current_arduino_label = arduino_label
				current_readable_label = readable_label
				current_cpu_types = []
			# see if it is a new model
			elif current_arduino_label is not None:
				search_object = re.search(current_arduino_label+".menu.cpu.[a-zA-Z0-9]*=", line)
				if search_object is not None: 
					cpu_model = search_object.group(0)[:-1].split(".")[-1]
					current_cpu_types.append(cpu_model)

		# add last entry
		if current_arduino_label is not None:
			arduino_model_data = [current_arduino_label,current_readable_label]
			arduino_model_data.append(current_cpu_types)
			models.append(tuple(arduino_model_data))

	return models

# Returns model list from boards.txt in specified directory
def get_boards_from_directory(fileloc,prefix):
	# models is a list of Model classes
	models = []
	with open(os.path.join(fileloc,"boards.txt"),'rb') as modelfile:

		still_expecting_menu_item_types = True
		
		# list for expected menu item types [(menu_item_type, menu_item_label), ...]
		expected_menu_item_types = []
		# keep track of current board info
		current_model = Model()
		
		for line in modelfile:
			# strip the line
			line = line.strip()
			# skip empty lines
			if len(line) == 0:
				continue
			# at the beginning of the file, we expect to see all the possible menu item types. Collect them
			if still_expecting_menu_item_types and current_model.board is None:
				menu_type_search_object = re.search("menu.[a-zA-Z0-9_-]*=(.*)", line)
				if menu_type_search_object is not None:
					# get menu item type + readable label
					expected_type_label,expected_readable_label = menu_type_search_object.group(0).split("=")
					expected_type_label = expected_type_label.split(".")[1]
					expected_menu_item_types.append((expected_type_label, expected_readable_label))
					continue
				
			# check if line depicts board name
			if ".name=" in line:
				# this is not a new menu item type line, so set expectation to False
				if still_expecting_menu_item_types:
					still_expecting_menu_item_types = False

				arduino_label,readable_label = line.strip().split(".name=")
				# check if we are on a different type of board now
				if current_model.board is not None and arduino_label != current_model.board:
					models.append(current_model)
					current_model = Model()
				# change the current labels
				current_model.board = arduino_label
				current_model.board_name = readable_label
				current_model.initialize_dict(expected_menu_item_types)
				current_model.set_prefix(prefix)

			# see if it is a different skew of current board type
			elif current_model.board is not None:
				search_object = re.search(current_model.board+".menu.[a-zA-Z0-9_-]*.[a-zA-Z0-9_-]*=(.*)", line)
				if search_object is not None:
					# figure out which menu type we got
					menu_item_type,menu_item_label = search_object.group(0).split("=")
					menu_item_type,menu_item_name = menu_item_type.split(".")[-2:]
					# add this menu_item_type + label to the proper item in current_menu_items
					current_model.add_menu_item(menu_item_type,menu_item_name,menu_item_label)

		# add last entry
		if current_model.board is not None:
			models.append(current_model)
			current_model = Model()

	return models


# A named tuple used to represent a specific menu item
MenuItem = namedtuple("MenuItem", ["name","label"])

# ModelData that is used to store label and all the subitems
class ModelData(object):
		def __init__(self, label):
			self.label = label
			self.items = []
			self.empty = True

		def is_empty(self):
			return self.empty

		def append(self, item):
			self.items.append(item)
			self.empty = False

		def __str__(self):
			return "'ModelData with Label: {} and Items: {}'".format(self.label,self.items)

		def __repr__(self):
			return str(self)

# Model that stores data for a particular arduino board
class Model(object):

	def __init__(self):
		self.board = None
		self.board_name = None
		self.menu_item_dict = OrderedDict()
		self.empty = True
		self.argument_prefix = ""

	# initialize menu item dictionary
	def initialize_dict(self, expected_menu_list):
		for menu_item_type,menu_item_label in expected_menu_list:
			self.menu_item_dict[menu_item_type] = ModelData(menu_item_label)

	# check if there are no items added to the dictionary
	def is_empty(self):
		return self.empty

	# set and get prefix
	def set_prefix(self, prefix):
		self.argument_prefix = prefix

	def get_prefix(self):
		return self.argument_prefix

	# add a menu item for a particular type
	def add_menu_item(self, menu_item_type, menu_item_name, menu_item_label):
		self.menu_item_dict[menu_item_type].append(MenuItem(menu_item_name,menu_item_label))
		self.empty = False

	def __str__(self):
		return "'Model with board: {}, board_name: {}, and item dict: {}".format(self.board,self.board_name,self.menu_item_dict)

	def __repr__(self):
		return str(self)
