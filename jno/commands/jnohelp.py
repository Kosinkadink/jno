from jno.commands.command import Command
from jno.commands.setdefault import SetDefault
from jno.commands.init import Init
from jno.commands.jnoserial import JnoSerial
from jno.commands.build import Build
from jno.commands.upload import Upload
from jno.commands.boards import Boards
from jno.commands.ports import Ports
from jno.commands.clean import Clean

import os
from colorama import Fore

command_list = [Init, Build, Upload, JnoSerial, Boards, Ports, Clean, SetDefault]

class JnoHelp(Command):

	help_name = "Help"
	help_usage = "jno help"
	help_description = "Prints usage and description of all supported commands"

	def run(self,argv,__location__):
		print(Fore.CYAN+"======================"+Fore.YELLOW)
		print("Help")
		print(Fore.CYAN+"----------------------")
		for command in command_list:
			print(self.formatted_help_string(command))
			if command != command_list[-1]:
				print("")
		print(Fore.CYAN+"======================"+Fore.RESET)

	@staticmethod
	def formatted_help_string(command):
		return """{3}{0}{4}:
    {5}Usage:{6} {1}
    {5}Description:{6} {2}{7}""".format(command.help_name,command.help_usage,command.help_description,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.GREEN,Fore.RESET)
