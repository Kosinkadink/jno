from jno.util import interpret_configs
from jno.util import run_arduino_process
from jno.util import create_build_directory
from jno.util import get_common_parameters
from jno.util import JnoException
from jno.util import verify_arduino_dir
from jno.commands.command import Command

import getopt

class Build(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs()
		verify_arduino_dir(jno_dict)
		create_build_directory(jno_dict)
		arg_list = self.perform_build(argv[1:],jno_dict)
		run_arduino_process(arg_list)

	# Create argument list for arduino build 
	def perform_build(self,argv,jno_dict):
		# assemble command query
		# GOAL: <arduino exec> --verify <script> --board <board>
		arg_list = [jno_dict["EXEC_SCRIPT"]]
		# add common params - set pref 
		arg_list.extend(get_common_parameters(jno_dict))
		# add build params
		arg_list.append("--verify")
		arg_list.append(jno_dict["SKETCH_INO"])
	
		try:
			opts,args = getopt.getopt(argv, '',['board=','verbose'])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		for opt, arg in opts:
			if opt in ("--board"):
				jno_dict["board"] = arg.strip()
			elif opt in ("--verbose"):
				arg_list.append("--verbose")

		# add board params
		arg_list.append("--board")
		arg_list.append(self.formatBoard(jno_dict["board"],jno_dict))

		return arg_list
