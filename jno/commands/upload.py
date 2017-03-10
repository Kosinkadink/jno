from jno.util import interpret_configs
from jno.util import run_arduino_process
from jno.util import move_libs
from jno.commands.command import Command

import getopt

class Upload(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		arg_list = self.perform_upload(argv[1:],jno_dict)
		move_libs(jno_dict)
		run_arduino_process(arg_list)


	# Create argument list for arduino build 
	def perform_upload(self,argv,jno_dict):
		# assemble command query
		# GOAL: <arduino exec> --upload <script> --board <board> --port <serial>
		arg_list = [jno_dict["EXEC_SCRIPT"]]
		# add upload params
		arg_list.append("--upload")
		arg_list.append(jno_dict["SKETCH_INO"])
	
		try:
			opts,args = getopt.getopt(argv, 'p:',['board=','port='])
		except getopt.GetoptError:
			print 'invalid arguments'
			quit()
		for opt, arg in opts:
			if opt in ("--board"):
				jno_dict["BOARD"] = "arduino:avr:"+arg.strip()
			elif opt in ("-p","--port"):
				jno_dict["PORT"] = arg.strip()

		# add board params
		arg_list.append("--board")
		arg_list.append(jno_dict["BOARD"])
		# add port params
		arg_list.append("--port")
		arg_list.append(jno_dict["PORT"])

		return arg_list
	