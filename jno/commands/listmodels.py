from jno.util import interpret_configs
from jno.commands.command import Command

import os
import re
from colorama import Fore

class ListModels(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		models = self.getAllModels(jno_dict)
		self.printAllModels(models)


	# Get and print list of all supported models
	def getAllModels(self,jno_dict):
		arduino_hardware_dir = os.path.join(jno_dict["EXEC_DIR"],"hardware/arduino/avr/")
		return self.getBoardsFromDirectory(arduino_hardware_dir)


	# Print each pair out nicely
	def printAllModels(self,models):
		print(Fore.CYAN + "")
		print("======================")
		print("SUPPORTED BOARD MODELS")
		print("----------------------")
		print("BOARD :: Board Name (cpu options)")
		for data in models:
			if len(data[2]) == 0:
				print("{0}{1}{2} :: {3}{4}{5}".format(Fore.YELLOW,data[0],Fore.CYAN,Fore.MAGENTA,data[1],Fore.CYAN))
			else:
				# Print cpus if there are any possible to specify
				print("{0}{1}{2} :: {3}{4}{5} (cpu={6}){7}".format(Fore.YELLOW,data[0],Fore.CYAN,Fore.MAGENTA,data[1],Fore.GREEN,','.join(data[2]),Fore.CYAN))
		print("======================")
		print(""+Fore.RESET)


	# Returns model list from boards.txt in specified directory
	def getBoardsFromDirectory(self,fileloc):
		# models is a list of tuples
		# [(arduino_label,readable_label,[cpu_type,...]),...]
		models = []
		with open(os.path.join(fileloc,"boards.txt"),'rb') as modelfile:
			current_arduino_label = None
			current_readable_label = None
			current_cpu_types = []
			for line in modelfile:
				if ".name=" in line:
					arduino_label,readable_label = line.strip().split(".name=")
					# check if we are on a different type of board now
					if current_arduino_label is not None and arduino_label != current_arduino_label:
						arduino_model_data = [current_arduino_label,current_readable_label]
						arduino_model_data.append(current_cpu_types)
						models.append(tuple(arduino_model_data))
					# change the current labels
					current_arduino_label = arduino_label
					current_readable_label = readable_label
					current_cpu_types = []
				# see if it is a new model
				elif current_arduino_label is not None:
					search_object = re.search(current_arduino_label+".menu.cpu.[a-z0-9]*=", line)
					if search_object is not None: 
						cpu_model = search_object.group(0)[:-1].split(".")[-1]
						current_cpu_types.append(cpu_model)

			# add last entry
			if current_arduino_label is not None and arduino_label != current_arduino_label:
				arduino_model_data = [current_arduino_label,current_readable_label]
				arduino_model_data.append(current_cpu_types)
				models.append(tuple(arduino_model_data))

		return models
