from jno.util import interpret_configs, get_all_models, JnoException
from jno.commands.command import Command

import os
import getopt
from sys import version_info
from colorama import Fore

class Boards(Command):

	help_name = "Boards"
	help_usage = "jno boards [-b, --board=] boardname"
	help_description = "Without arguments, prints list of all supported boards. With -b, prints details about specific board."

	def run(self,argv,location):
		jno_dict = interpret_configs()
		models = get_all_models(jno_dict)
		self.perform_boards(argv,models)

	def perform_boards(self,argv,models):
		try:
			opts,args = getopt.getopt(argv, 'b:', ['board='])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		# if a board is provided, show info about it
		for opt, arg in opts:
			if opt in ("-b","--board"):
				return self.print_model_data(arg,models)
		# otherwise, list all models
		self.print_all_models(models)

	def create_parameter_string(self,model):
		parameter_types = []
		parameter_string = ""

		if not model.is_empty():
			if version_info < (3,0): # python2 code
				for item_type,data in model.menu_item_dict.iteritems():
					if not data.is_empty():
						parameter_types.append(item_type)
			else: # python3 code
				for item_type,data in model.menu_item_dict.items():
					if not data.is_empty():
						parameter_types.append(item_type)

			parameter_string = ",".join(parameter_types)

			if len(parameter_string) > 0:
				parameter_string = "(" + parameter_string + ")"

		return parameter_string

	# Print each pair out nicely
	def print_all_models(self,models):
		print(Fore.CYAN+"======================")
		print("{3}{0}{4} :: {5}{1} {6}{2}{4}".format("Board","Board Name","(parameter types)",Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN)) 
		print("----------------------")
		for model in models:
			# show relevant info, so see if any parameters exist for board
			parameter_string = self.create_parameter_string(model)
			print("{3}{0}{4} :: {5}{1} {6}{2}{4}".format(model.board,model.board_name,parameter_string,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN))
		# finish up the printing
		print("======================"+Fore.RESET)

	def print_model_data(self,board,models):
		# see if board exists
		relevant_model = None
		for model in models:
			if model.board == board:
				relevant_model = model
				break
		if relevant_model is None:
			raise JnoException("board '{}' is not recognized".format(board))

		print(Fore.CYAN+"======================")
		print("Board: {2}{0}{4} ({1}){3}".format(relevant_model.board,relevant_model.board_name,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA))
		print("  Prefix: {1}{0}{2}".format(relevant_model.get_prefix(),Fore.YELLOW,Fore.CYAN))
		# if model has relevant parameter values, show them
		if not relevant_model.is_empty():
			if version_info < (3,0): # python2 code
				for item_type,data in relevant_model.menu_item_dict.iteritems():
					self.print_parameters_with_values(item_type,data)
			else: # python3 code
				for item_type,data in relevant_model.menu_item_dict.items():
					self.print_parameters_with_values(item_type,data)
		print("======================"+Fore.RESET)

	# Print out parameter with all possible values
	def print_parameters_with_values(self,item_type,data):
		# if this parameter has relevant values, show them
		if not data.is_empty():
			print("  Parameter: {2}{0}{3} ({1}){4}".format(item_type,data.label,Fore.GREEN,Fore.MAGENTA,Fore.CYAN))
			# parse through possible values
			for item in data.items:
				print("    {2}{0}{3} ({1}){4}".format(item.name,item.label,Fore.YELLOW,Fore.MAGENTA,Fore.CYAN))
