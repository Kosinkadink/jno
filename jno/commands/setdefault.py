from jno.util import parse_jno_file,valid_params
from jno.util import verify_arduino_dir
from jno.util import formatted_help_string
from jno.util import JnoException
from jno.commands.command import Command

import getopt
import os
from sys import version_info
from colorama import Fore

class SetDefault(Command):

	help_name = "SetDefault"
	help_usage = "jno setlocal|setglobal [--exec_dir=] arduino_dir [--baudrate=] baudrate [--port=] port [--board=] boardname"
	help_description = "Sets local or global default values for various parameters. At least one argument must be provided. Exec_dir refers to the Arduino directory (most OS) or app (MacOS only)."

	def __init__(self,argv,location,file_name="jno.jno"):
		if argv and argv[-1] == "help":
			print(formatted_help_string(self,surround=True))
			return
		self.run(argv,location,file_name)

	# Reads current .jno file, applies requested changes
	def run(self,argv,location,file_name="jno.jno"):
		jno_dict = {}
		jno_dict = parse_jno_file(jno_dict,location,file_name)

		try:
			opts,args = getopt.getopt(argv,'',['exec_dir=','baudrate=','port=','board='])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		
		for opt, arg in opts:
			opt = opt[2:].lower()
			if opt in valid_params:
				jno_dict[opt] = arg
				if opt == "exec_dir":
					verify_arduino_dir(jno_dict)
				print("{2}New default {3}{0}{4}: {5}{1}{6}".format(opt,arg,Fore.YELLOW,Fore.MAGENTA,Fore.CYAN,Fore.GREEN,Fore.RESET))

		if opts:
			self.create_new_jno_file(jno_dict,location,file_name)
		else:
			print(Fore.YELLOW+"No settings given to save, no changes made"+Fore.RESET)

	# Overwrites current .jno file
	def create_new_jno_file(self,jno_dict,location,file_name):
		with open(os.path.join(location,file_name),'w') as jno:
			if version_info < (3,0): # python2 code
				for key,value in jno_dict.iteritems():
					jno.write("{0}=={1}\n".format(key,value))
			else: # python3 code
				for key,value in jno_dict.items():
					jno.write("{0}=={1}\n".format(key,value))