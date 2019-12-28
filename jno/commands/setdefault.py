from jno.util import parse_jno_file,valid_params
from jno.util import verify_arduino_dir
from jno.util import JnoException
from jno.commands.command import Command

import getopt
import os
from sys import version_info

class SetDefault(Command):

	def __init__(self,argv,location,file_name="jno.jno"):
		self.run(argv,location,file_name)

	# Reads current .jno file, applies requested changes
	def run(self,argv,location,file_name="jno.jno"):
		jno_dict = {}
		jno_dict = parse_jno_file(jno_dict,location,file_name)

		# get lowercase versions as well
		opt_arg_list = ['exec_dir=','baudrate=','port=','board=']
		for n in range(0,len(opt_arg_list)):
			opt_arg_list.append(opt_arg_list[n].lower())

		try:
			opts,args = getopt.getopt(argv,'',opt_arg_list)
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		
		for opt, arg in opts:
			opt = opt[2:].lower()
			if opt in valid_params:
				jno_dict[opt] = arg
				if opt == "exec_dir":
					verify_arduino_dir(jno_dict)
				print('New default {0}: {1}'.format(opt,arg))

		self.create_new_jno_file(jno_dict,location,file_name)

	# Overwrites current .jno file
	def create_new_jno_file(self,jno_dict,location,file_name):
		with open(os.path.join(location,file_name),'w') as jno:
			if version_info < (3,0): # python2 code
				for key,value in jno_dict.iteritems():
					jno.write('{0}=={1}\n'.format(key,value))
			else: # python3 code
				for key,value in jno_dict.items():
					jno.write('{0}=={1}\n'.format(key,value))