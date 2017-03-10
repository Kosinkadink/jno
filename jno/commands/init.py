
from jno.commands.command import Command

import os

class Init(Command):

	def run(self,argv,location):
		self.init_jno(location)

	def init_jno(self,jno_dir):
		lib_dir = os.path.join(jno_dir,'lib')
		sketch_dir = os.path.join(jno_dir,'sketch')
		jno_file = os.path.join(jno_dir,'jno.jno')
		# create lib if does not exist
		if not os.path.exists(lib_dir):
			os.mkdir(lib_dir)
		# create sketch if does not exist
		if not os.path.exists(sketch_dir):
			os.mkdir(sketch_dir)
		# create jno.jno 
		if not os.path.exists(jno_file):
			with open(jno_file,'wb') as jno:
				jno.write("EXEC_DIR==NULL\n")
				jno.write("EXEC_LIBS==DEFAULT\n")
				jno.write("BOARD==arduino:avr:uno\n")
				jno.write("BAUDRATE==9600\n")
				jno.write("PORT==DEFAULT\n")
				jno.write("SKETCH_DIR==DEFAULT\n")
		print 'directories and .jno initialized'
