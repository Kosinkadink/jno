
from jno.commands.command import Command

import os

class Init(Command):

	def run(self,argv,location):
		self.init_jno(location)

	def init_jno(self,jno_dir):
		lib_dir = os.path.join(jno_dir,'libraries')
		lib_dir_old = os.path.join(jno_dir,'lib')
		sketch_dir = os.path.join(jno_dir,'sketch')
		jno_file = os.path.join(jno_dir,'jno.jno')
		# create lib if does not exist
		if not os.path.exists(lib_dir):
			# check if we need to rename
			if os.path.isdir(lib_dir_old):
				os.rename(lib_dir_old, lib_dir)
			else:
				os.mkdir(lib_dir)
				# create putlibrarieshere.txt file, useful when using with git so directory gets committed
				with open(os.path.join(lib_dir,"putlibrarieshere.txt"),"wb") as libfile:
					pass

		# create sketch if does not exist
		if not os.path.exists(sketch_dir):
			os.mkdir(sketch_dir)
			# create sketch.ino in sketch dir with setup/loop functions
			with open(os.path.join(sketch_dir,"sketch.ino"),"wb") as sketchfile:
				sketchfile.write("void setup() {\n\n}\n")
				sketchfile.write("void loop() {\n\n}\n")

		# create jno.jno 
		if not os.path.exists(jno_file):
			with open(jno_file,'wb') as jno:
				jno.write("EXEC_DIR==NULL\n")
				jno.write("BOARD==uno\n")
				jno.write("BAUDRATE==9600\n")
				jno.write("PORT==DEFAULT\n")
				jno.write("SKETCH_DIR==DEFAULT\n")
		print('directories and .jno initialized')
