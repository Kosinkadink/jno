#!/usr/bin/python2

class Command():

	def __init__(self,argv,location):
		self.run(argv,location)


	# Overload this function in actual commands
	def run(self,argv,location):
		pass


	# Return proper board formatting
	def formatBoard(self,board):
		if not board.startswith("arduino:avr:"):
			return "arduino:avr:"+board
		return board
