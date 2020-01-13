from jno.util import interpret_configs
from jno.util import run_arduino_process
from jno.util import create_build_directory
from jno.util import get_common_parameters
from jno.util import verify_arduino_dir
from jno.util import verify_and_get_port
from jno.util import JnoException
from jno.commands.command import Command

import getopt
from colorama import Fore

class Upload(Command):

	help_name = "Upload"
	help_usage = "jno upload [-b, --board=] boardname [-p, --ports=] port [-v, --verbose]"
	help_description = "Runs build and uploads to board. Without arguments, uses board/port defined locally/globally. " \
		"If port is not defined, uses first available port. With -v, more info will be displayed during upload."

	def run(self,argv,location):
		jno_dict = interpret_configs()
		verify_arduino_dir(jno_dict)
		create_build_directory(jno_dict)
		arg_list = self.perform_upload(argv,jno_dict)
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
			opts,args = getopt.getopt(argv, 'b:p:v',['board=','port=','verbose'])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		for opt, arg in opts:
			if opt in ("-b","--board"):
				jno_dict["board"] = arg.strip()
			elif opt in ("-p","--port"):
				jno_dict["port"] = arg.strip()
			elif opt in ("-v","--verbose"):
				arg_list.append("--verbose")
		# verify port or get first available
		port = verify_and_get_port(jno_dict["port"])
		if not port:
			if jno_dict["port"] == "DEFAULT":
				raise JnoException("no ports available")
			raise JnoException("port does not exist: {}".format(jno_dict["port"]))
		else:
			if jno_dict["port"] == "DEFAULT":
				print("{1}No port provided, using available port {0}{2}".format(port,Fore.YELLOW,Fore.RESET))

		# add board params
		arg_list.append("--board")
		arg_list.append(self.formatBoard(jno_dict["board"],jno_dict))
		# add port params
		arg_list.append("--port")
		arg_list.append(port)

		return arg_list
