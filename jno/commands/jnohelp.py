from jno.commands.command import Command
from jno.commands.setdefault import SetDefault
from jno.commands.init import Init
from jno.commands.jnoserial import JnoSerial
from jno.commands.build import Build
from jno.commands.upload import Upload
from jno.commands.boards import Boards
from jno.commands.ports import Ports
from jno.commands.clean import Clean
from jno.util import formatted_help_string, JnoException

import os
from colorama import Fore

command_list = [Init, Build, Upload, JnoSerial, Boards, Ports, Clean, SetDefault]

class JnoHelp(Command):

	help_name = "Help"
	help_usage = "jno help [command_name]"
	help_description = "Without arguments, prints usage and description for all supported commands. With a command name supplied, prints usage and description for specific command."

	def run(self,argv,location):
		if len(argv) > 0:
			query_name = argv[-1]
			found_command = None
			if query_name in ["setlocal", "setglobal"]:
				found_command = SetDefault
			else:
				for command in command_list:
					if command.help_name.lower() == query_name.lower():
						found_command = command
						break
			if not found_command:
				raise JnoException("help for command '{}' cannot be displayed'; command not found".format(query_name))
			print(formatted_help_string(found_command,surround=True))
			return

		print(Fore.CYAN+"======================")
		for command in command_list:
			print(formatted_help_string(command))
			print(Fore.CYAN+"----------------------")
		print(formatted_help_string(self))
		print(Fore.CYAN+"======================"+Fore.RESET)
