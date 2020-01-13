from jno.commands.command import Command
from jno.util import create_default_jno_file

import os

class Init(Command):

	help_name = "Init"
	help_usage = "jno init"
	help_description = "Initializes current directory for jno purposes; adds sketch dir and empty .ino file, adds libraries dir, and adds default jno.jno file."

	def run(self,argv,location):
		self.init_jno(location)

	def init_jno(self,jno_dir):
		lib_dir = os.path.join(jno_dir,"libraries")
		lib_dir_old = os.path.join(jno_dir,"lib")
		sketch_dir = os.path.join(jno_dir,"sketch")
		jno_file_name = "jno.jno"
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
			with open(os.path.join(sketch_dir,"sketch.ino"),"w") as sketchfile:
				sketchfile.write("void setup() {\n\n}\n")
				sketchfile.write("void loop() {\n\n}\n")

		# create jno.jno 
		if not os.path.exists(os.path.join(jno_dir,jno_file_name)):
			create_default_jno_file(jno_dir,jno_file_name)
		print('directories and .jno initialized')
