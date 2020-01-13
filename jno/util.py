import os
import sys
import re
import shutil
import subprocess
try:
	import serial.tools.list_ports
except ImportError:
	list_ports_supported = False
else:
	list_ports_supported = True
from sys import platform
from shutil import rmtree
from collections import OrderedDict, namedtuple
from colorama import Fore


# Parameters to be included in .jno
valid_params = {
		'exec_dir',
		'board',
		'port',
		'baudrate',
		'sketch_dir'
	}

# Global jno settings file name
global_file_name = ".jnoglobal.jno"

# Exception class for jno-related exceptions
class JnoException(Exception):
	pass

# Replaces temporary dictionary values with actual values
def interpret_configs():
	jno_dict = read_configs(get_home_directory(),global_file_name)
	# based on operating system, try to use a default location if no exec_dir is set
	if jno_dict["exec_dir"] in ('NULL','DEFAULT'):
		if os.name == 'nt': # running on Windows
			if os.path.isdir("C:/Program Files (x86)/Arduino"):
				jno_dict["exec_dir"] = "C:/Program Files (x86)/Arduino"
		elif platform == "darwin": # running on OS X
			if os.path.isdir("/Applications/Arduino.app"):
				jno_dict["exec_dir"] = "/Applications/Arduino.app"
		# otherwise, if still don't have a value, raise exception
		if jno_dict["exec_dir"] in ('NULL','DEFAULT'):
			raise JnoException("exec_dir has not been initialized (use jno setglobal --exec_dir=[Installed Arduino Directory])")
		
	# perform necessary additions/replacements
	if jno_dict["sketch_dir"] == 'DEFAULT':
		jno_dict["sketch_dir"] = os.getcwd()
	# if not absolute directory, make it local
	elif not jno_dict["sketch_dir"].startswith('/'):
		jno_dict["sketch_dir"] = os.path.join(os.getcwd(),jno_dict["sketch_dir"])
	# create EXEC_SCRIPT; if on Windows, uses the better executable
	if os.name == 'nt':
		jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["exec_dir"],'arduino_debug')
	elif platform == "darwin": # if on OS X, use proper executable directory
		jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["exec_dir"],"Contents/MacOS/Arduino")
	else:
		jno_dict["EXEC_SCRIPT"] = os.path.join(jno_dict["exec_dir"],"arduino")
	# create SKETCH_INO
	jno_dict["SKETCH_INO"] = os.path.join(jno_dict["sketch_dir"],'sketch/sketch.ino')
	# create SKETCH_LIBS
	jno_dict["SKETCH_LIBS"] = os.path.join(jno_dict["sketch_dir"],'libraries')
	
	return jno_dict

# Verify that exec_dir is pointing at a valid arduino
def verify_arduino_dir(jno_dict):
	exec_dir = jno_dict["exec_dir"]
	if not os.path.isdir(exec_dir):
		raise JnoException("specified exec_dir is not a valid directory: {}".format(exec_dir))
	if platform == "darwin": # running on OS X
		revision_file = os.path.join(exec_dir,"Contents/Java/revisions.txt")
	else:
		revision_file = os.path.join(exec_dir,"revisions.txt")
	if not os.path.exists(revision_file):
		raise JnoException("specified exec_dir is not pointing at a valid arduino install: {}".format(exec_dir))

# Create global settings in home directory if not created already
def create_global_settings():
	if not os.path.exists(os.path.join(get_home_directory(),global_file_name)):
		create_default_jno_file(get_home_directory(),global_file_name)

# Write default jno file in desired location
def create_default_jno_file(location,file_name):
	with open(os.path.join(location,file_name),'w') as jno:
		jno.write("exec_dir==NULL\n")
		jno.write("board==uno\n")
		jno.write("baudrate==9600\n")
		jno.write("port==DEFAULT\n")
		jno.write("sketch_dir==DEFAULT\n")

# Parses global and local .jno, returning dictionary
def read_configs(global_location,file_name):
	jno_dict = {}
	jno_dict = parse_jno_file(jno_dict,global_location,file_name)
	if os.path.exists(os.path.join(os.getcwd(),"jno.jno")):
		jno_dict = parse_jno_file(jno_dict,os.getcwd())
	return jno_dict


# Parses .jno file in given directory, returning dictionary
def parse_jno_file(jno_dict,jno_dir,file_name="jno.jno"):
	new_dict = {}

	with open(os.path.join(jno_dir,file_name),'r') as jno:
		for line in jno:
			line = line.strip()
			if len(line) == 0:
				continue
			param,conf_input = line.split('==')
			param = param.lower()
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


# Run arduino with an assembled argument list stdout=subprocess.PIPE, 
def run_arduino_process(arg_list):
	try:
		call = subprocess.Popen(arg_list, stderr=subprocess.PIPE, universal_newlines=True)
		for line in call.stderr:
			if line.startswith("TRACE") or line.startswith("DEBUG") or line.startswith("INFO"):
				continue
			elif line[25:29] == "INFO" or line[25:29] == "WARN":
				continue
			else:
				sys.stdout.write(line)
		# wait until call is finished
		call.communicate()[0]
	except subprocess.CalledProcessError as e:
		returned = e.returncode
	print(Fore.YELLOW + 'All Actions Complete: {}'.format(return_code_qualifier(call.returncode)) + Fore.RESET)


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
	build_directory = os.path.join(jno_dict["sketch_dir"],".build")
	if not os.path.isdir(build_directory):
		os.mkdir(build_directory)
	# while we are at it, check if library directory has the right name
	lib_dir = os.path.join(jno_dict["sketch_dir"],"libraries")
	lib_dir_old = os.path.join(jno_dict["sketch_dir"],"lib")
	if os.path.isdir(lib_dir_old):
		os.rename(lib_dir_old,lib_dir)

# Get home directory of current user
def get_home_directory():
	return os.path.expanduser('~')

# Returns list of common parameters needed for upload/build
def get_common_parameters(jno_dict):
	# we are trying to set the build and sketchbook path
	build_path = os.path.join(jno_dict["sketch_dir"],".build")
	sketchbook_path = jno_dict["sketch_dir"]
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

# Get all ports to connected devices
def get_all_ports():
	if list_ports_supported:
		return serial.tools.list_ports.comports()
	print("port listing is not supported with current version of pyserial")
	return None

# Get first port name
def get_first_port_name():
	ports = get_all_ports()
	if ports:
		return ports[0].device
	return None

# Check if port exists; if default, use first available port
def verify_and_get_port(port_name,use_first=True):
	if port_name == "DEFAULT":
		if use_first:
			return get_first_port_name()
		return None
	ports = get_all_ports()
	for port in ports:
		if port.device == port_name:
			return port_name
	return None

# Get and print list of all supported models
def get_all_models(jno_dict):
	# directores to ignore
	ignore_dirs = ["tools"]
	# get hardware directory
	if platform == "darwin": # if running on a OS X
		arduino_hardware_dir = os.path.join(jno_dict["exec_dir"],"Contents/Java/hardware")
	else: # running on all other platforms
		arduino_hardware_dir = os.path.join(jno_dict["exec_dir"],"hardware")
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
	#arduino_hardware_dir = os.path.join(jno_dict["exec_dir"],"hardware/arduino/avr/")
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

# Get help string for command
def formatted_help_string(command, surround=False):
		return """{8}{3}{0}:
    {4}Usage:{6} {1}
    {4}Description:{5} {2}{9}{7}""".format(
    	command.help_name,command.help_usage,command.help_description,
    	Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN,Fore.RESET,
    	Fore.CYAN+"======================\n" if surround else "",
    	Fore.CYAN+"\n======================" if surround else "")

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
		return "Model with board: {}, board_name: {}, and item dict: {}".format(self.board,self.board_name,self.menu_item_dict)

	def __repr__(self):
		return str(self)
