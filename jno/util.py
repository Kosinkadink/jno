import os
import re
import shutil
import subprocess
from shutil import rmtree
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
	# create EXEC_SCRIPT; if on Windows, uses the better executable
	if os.name == 'nt':
		jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["EXEC_DIR"],'arduino_debug')
	else:
		jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["EXEC_DIR"],"arduino")
	# create SKETCH_INO
	jno_dict["SKETCH_INO"] = os.path.join(jno_dict["SKETCH_DIR"],'sketch/sketch.ino')
	# create SKETCH_LIBS
	jno_dict["SKETCH_LIBS"] = os.path.join(jno_dict["SKETCH_DIR"],'libraries')

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

	with open(os.path.join(jno_dir,'jno.jno'),'r') as jno:
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


# Cleans selected directory
def clean_directory(dir_to_clean):
	# if exists, remove and replace
	if os.path.isdir(dir_to_clean):
		try:
			rmtree(dir_to_clean)
		except:
			return False
	# in either case, make the directory again
	try:
		os.mkdir(dir_to_clean)
	except:
		return False
	return True 


# Run arduino with an assembled argument list
def run_arduino_process(arg_list):
	try:
		returned = subprocess.check_call(arg_list)
	except subprocess.CalledProcessError as e:
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

# Create directory for building
def create_build_directory(jno_dict):
	build_directory = os.path.join(jno_dict["SKETCH_DIR"],".build")
	if not os.path.isdir(build_directory):
		os.mkdir(build_directory)
	# while we are at it, check if library directory has the right name
	lib_dir = os.path.join(jno_dict["SKETCH_DIR"],"libraries")
	lib_dir_old = os.path.join(jno_dict["SKETCH_DIR"],"lib")
	if os.path.isdir(lib_dir_old):
		os.rename(lib_dir_old,lib_dir)

# Returns list of common parameters needed for upload/build
def get_common_parameters(jno_dict):
	# we are trying to set the build and sketchbook path
	build_path = os.path.join(jno_dict["SKETCH_DIR"],".build")
	sketchbook_path = jno_dict["SKETCH_DIR"]
	pref_string_list = []
	argument_list = []
	# fill out string list
	pref_string_list.append("build.path={}".format(build_path))
	pref_string_list.append("sketchbook.path={}".format(sketchbook_path))
	# fill out argument list
	for pref_string in pref_string_list:
		argument_list.append("--pref")
		argument_list.append(pref_string)
	# return arguments
	return argument_list

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
def get_boards_from_directory(fileloc,prefix):
	# models is a list of Model classes
	models = []
	with open(os.path.join(fileloc,"boards.txt"),'r') as modelfile:

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

		def get_first(self):
			if len(self.items) > 0:
				return self.items[0]
			else:
				return None

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
