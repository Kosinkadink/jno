from jno.util import parse_jno_file,valid_params
from jno.commands.command import Command

import getopt
import os

class SetDefault(Command):

	# Reads current .jno file, applies requested changes
	def run(self,argv,location):
		jno_dict = {}
		jno_dict = parse_jno_file(jno_dict,location)

		# get lowercase versions as well
		opt_arg_list = ['EXEC_DIR=','EXEC_LIBS=','BAUDRATE=','PORT=','BOARD=']
		for n in range(0,len(opt_arg_list)):
			opt_arg_list.append(opt_arg_list[n].lower())

		try:
			opts,args = getopt.getopt(argv[1:],'',opt_arg_list)
		except getopt.GetoptError:
			print 'invalid arguments'
			quit()
		
		for opt, arg in opts:
			opt = opt[2:].upper()
			if opt in valid_params:
				jno_dict[opt] = arg
				print 'New default {0}: {1}'.format(opt,arg)

		self.create_new_jno_file(jno_dict,location)

	# Overwrites current .jno file
	def create_new_jno_file(self,jno_dict,location):
		with open(os.path.join(location,'jno.jno'),'wb') as jno:
			for key,value in jno_dict.iteritems():
				jno.write('{0}=={1}\n'.format(key,value))