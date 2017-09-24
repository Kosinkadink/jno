#!/usr/bin/python2
from jno.util import get_all_models
from colorama import Fore


class Command():

	def __init__(self,argv,location):
		self.run(argv,location)


	# Overload this function in actual commands
	def run(self,argv,location):
		pass


	# Return proper board formatting
	def formatBoard(self,board,jno_dict):
		prepared_board_string = None
		board_name = None
		if not board.startswith("arduino:avr:"):
			prepared_board_string = "arduino:avr:{}".format(board)
		else:
			prepared_board_string = board
			board_name = prepared_board_string.split(":")[2]
		# Check if CPU was explicitly specified; if not, check if one can be given
		if ":cpu=" not in prepared_board_string:
			all_boards = get_all_models(jno_dict)
			for board_data in all_boards:
				# If board exists...
				if board_data[0] == board_name:
					cpu_names = board_data[2]
					# Add the first CPU option if available
					if len(cpu_names) > 0:
						prepared_board_string += ":cpu={}".format(cpu_names[0])
						print("{1}Using default {2}cpu={0}{3}".format(cpu_names[0],Fore.YELLOW,Fore.CYAN,Fore.RESET))
		return prepared_board_string
