from jno.util import interpret_configs
from jno.util import clean_directory
from jno.commands.command import Command

import os
from colorama import Fore

class Clean(Command):

	help_name = "Clean"
	help_usage = "jno clean"
	help_description = "Cleans cached .build directory, contained inside sketch_dir for current directory."

	def run(self,argv,location):
		jno_dict = interpret_configs()
		if clean_directory(os.path.join(jno_dict["sketch_dir"],".build")):
			print("{}Cleaned build files successfully{}".format(Fore.GREEN,Fore.RESET))
		else:
			print("{}Could not clean build files{}".format(Fore.RED,Fore.RESET))
