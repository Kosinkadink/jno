#!/usr/bin/python2

class Command():

	def __init__(self,argv,location):
		self.run(argv,location)

	# Overload this function in actual commands
	def run(self,argv,location):
		pass