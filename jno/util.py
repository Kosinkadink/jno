import os
import shutil
import subprocess


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
				print 'Copied lib {}'.format(item)


# Run arduino with an assembled argument list
def run_arduino_process(arg_list):
	try:
		returned = subprocess.check_call(arg_list)
	except subprocess.CalledProcessError,e:
		returned = e.returncode
	print 'ALL ACTIONS COMPLETED: {}'.format(return_code_qualifier(returned))


# Returns meaning of return code
def return_code_qualifier(return_code):
	return_code_dict = {
		0:"Success",
		1:"Build failed or upload failed",
		2:"Sketch not found",
		3:"Invalid argument for commandline option",
		4:"Preference passed to --get-pref does not exist"
	}
	return return_code_dict[return_code]
