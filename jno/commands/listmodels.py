from jno.util import interpret_configs, get_all_models, JnoException
from jno.commands.command import Command

import os
from sys import version_info
import getopt
from colorama import Fore

class ListModels(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		models = get_all_models(jno_dict)
		self.perform_listmodels(argv[1:],models)

	def perform_listmodels(self,argv,models):
		is_board_provided = False
		try:
			opts,args = getopt.getopt(argv, '', ['board='])
		except getopt.GetoptError:
			raise JnoException("invalid arguments")
		# if a board is provided, show info about it
		for opt, arg in opts:
			if opt in ("--board"):
				is_board_provided = True
				self.printDataAboutModel(arg,models)
		# otherwise, list all models
		if not is_board_provided:
			self.printAllModels(models)

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
	def printAllModels(self,models):
		print(Fore.CYAN + "")
		print("======================")
		print("SUPPORTED BOARD MODELS")
		print("----------------------")
		print("{3}{0}{4} :: {5}{1} {6}{2}{4}".format("Board","Board Name","(parameter types)",Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN)) 
		print("----------------------")
		for model in models:
			# show relevant info, so see if any parameters exist for board
			parameter_string = self.create_parameter_string(model)
			print("{3}{0}{4} :: {5}{1} {6}{2}{4}".format(model.board,model.board_name,parameter_string,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN))
		# finish up the printing
		print("======================")
		print(""+Fore.RESET)

	def printDataAboutModel(self,board,models):
		# see if board exists
		relevant_model = None
		for model in models:
			if model.board == board:
				relevant_model = model
				break
		if relevant_model is None:
			raise JnoException("board '{}' is not recognized".format(board))

		print(Fore.CYAN + "")
		print("======================")
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
		print("======================")
		print(""+Fore.RESET)

	# Print out parameter with all possible values
	def print_parameters_with_values(self,item_type,data):
		# if this parameter has relevant values, show them
		if not data.is_empty():
			print("  Parameter: {2}{0}{3} ({1}){4}".format(item_type,data.label,Fore.GREEN,Fore.MAGENTA,Fore.CYAN))
			# parse through possible values
			for item in data.items:
				print("    {2}{0}{3} ({1}){4}".format(item.name,item.label,Fore.YELLOW,Fore.MAGENTA,Fore.CYAN))




