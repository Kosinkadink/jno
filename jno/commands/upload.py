from jno.util import interpret_configs
from jno.util import run_arduino_process
from jno.util import create_build_directory
from jno.util import get_common_parameters
from jno.util import JnoException
from jno.commands.command import Command

import getopt

class Upload(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		create_build_directory(jno_dict)
		arg_list = self.perform_upload(argv[1:],jno_dict)
		run_arduino_process(arg_list)

	# Create argument list for arduino build 
	def perform_upload(self,argv,jno_dict):
		# assemble command query
		# GOAL: <arduino exec> --upload <script> --board <board> --port <serial>
		arg_list = [jno_dict["EXEC_SCRIPT"]]
		# add common params - set pref 
		arg_list.extend(get_common_parameters(jno_dict))
		# add upload params
		arg_list.append("--upload")
		arg_list.append(jno_dict["SKETCH_INO"])
	
		try:
			opts,args = getopt.getopt(argv, 'p:',['board=','port='])
		except getopt.GetoptError:
			raise JnoException("invalid arguments")
		for opt, arg in opts:
			if opt in ("--board"):
				jno_dict["BOARD"] = arg.strip()
			elif opt in ("-p","--port"):
				jno_dict["PORT"] = arg.strip()
			elif opt in ("--verbose"):
				arg_list.append("--verbose")

		# add board params
		arg_list.append("--board")
		arg_list.append(self.formatBoard(jno_dict["BOARD"],jno_dict))
		# add port params
		arg_list.append("--port")
		arg_list.append(jno_dict["PORT"])

		return arg_list
