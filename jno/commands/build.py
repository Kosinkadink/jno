from jno.util import interpret_configs
from jno.util import run_arduino_process
from jno.util import move_libs
from jno.commands.command import Command

import getopt

class Build(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		arg_list = self.perform_build(argv[1:],jno_dict)
		move_libs(jno_dict)
		run_arduino_process(arg_list)


	# Create argument list for arduino build 
	def perform_build(self,argv,jno_dict):
		# assemble command query
		# GOAL: <arduino exec> --verify <script> --board <board>
		arg_list = [jno_dict["EXEC_SCRIPT"]]
		# add build params
		arg_list.append("--verify")
		arg_list.append(jno_dict["SKETCH_INO"])
	
		try:
			opts,args = getopt.getopt(argv, '',['board='])
		except getopt.GetoptError:
			print 'invalid arguments'
			quit()
		for opt, arg in opts:
			if opt in ("--board"):
				jno_dict["BOARD"] = "arduino:avr:"+arg.strip()

		# add board params
		arg_list.append("--board")
		arg_list.append(jno_dict["BOARD"])

		return arg_list
				