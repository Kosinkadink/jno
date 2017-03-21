from jno.util import interpret_configs
from jno.commands.command import Command

import os

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
		print ""
		print "======================"
		print "SUPPORTED BOARD MODELS"
		print "----------------------"
		print "BOARD :: Board Name"
		for pair in models:
			print "{0} :: {1}".format(pair[0],pair[1])
		print "======================"
		print ""


	# Returns model list from boards.txt in specified directory
	def getBoardsFromDirectory(self,fileloc):
		# models is a list of tuples
		# [(arduino_label,readable_label),...]
		models = []
		with open(os.path.join(fileloc,"boards.txt"),'rb') as modelfile:
			for line in modelfile:
				if ".name=" in line:
					arduino_label,readable_label = line.strip().split(".name=")
					models.append((arduino_label,readable_label))
		return models


	#TODO: get possible parameters for each board
