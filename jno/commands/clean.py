from jno.util import interpret_configs
from jno.util import clean_directory
from jno.commands.command import Command

import os
from colorama import Fore

class Clean(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		if clean_directory(os.path.join(jno_dict["SKETCH_DIR"],".build")):
			print("{}Cleaned build files successfully{}".format(Fore.GREEN,Fore.RESET))
		else:
			print("{}Could not clean build files{}".format(Fore.RED,Fore.RESET))
