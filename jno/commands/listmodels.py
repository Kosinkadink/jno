from jno.util import interpret_configs, get_all_models
from jno.commands.command import Command

import os
from colorama import Fore

class ListModels(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		models = get_all_models(jno_dict)
		self.printAllModels(models)


	# Print each pair out nicely
	def printAllModels(self,models):
		print(Fore.CYAN + "")
		print("======================")
		print("SUPPORTED BOARD MODELS")
		print("----------------------")
		print("BOARD :: Board Name (cpu options)")
		for data in models:
			# If there are no cpu options, only show board and board name
			if len(data[2]) == 0:
				print("{2}{0}{3} :: {4}{1}{3}".format(data[0],data[1],Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.CYAN))
			else:
				# Print cpus if there are any possible to specify
				print("{3}{0}{4} :: {5}{1}{6} (cpu={2}){4}".format(data[0],data[1],','.join(data[2]),Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN))
		print("======================")
		print(""+Fore.RESET)
