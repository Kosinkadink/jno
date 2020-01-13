import sys
import os
from colorama import init, Fore

import jno.commands
from jno.commands.setdefault import SetDefault
from jno.commands.init import Init
from jno.commands.jnoserial import JnoSerial
from jno.commands.build import Build
from jno.commands.upload import Upload
from jno.commands.boards import Boards
from jno.commands.ports import Ports
from jno.commands.clean import Clean
from jno.commands.jnohelp import JnoHelp
from jno.util import create_global_settings
from jno.util import global_file_name
from jno.util import get_home_directory
from jno.util import JnoException

if os.name == 'nt':
	init()


DEBUG = False


def init_command(argv):
	Init(argv,os.getcwd())

def build_command(argv):
	Build(argv)

def upload_command(argv):
	Upload(argv)

def serial_command(argv):
	JnoSerial(argv)

def setglobal_command(argv):
	SetDefault(argv,get_home_directory(),global_file_name)

def setlocal_command(argv):
	SetDefault(argv,os.getcwd())

def boards_command(argv):
	Boards(argv)

def ports_command(argv):
	Ports(argv)

def clean_command(argv):
	Clean(argv)

def help_command(argv):
	JnoHelp(argv)


# Dictionary linking option to function
command_dict = {
	"init": init_command,
	"build": build_command,
	"upload": upload_command,
	"serial": serial_command,
	"setglobal": setglobal_command,
	"setlocal": setlocal_command,
	"boards": boards_command,
	"ports": ports_command,
	"clean": clean_command,
	"help": help_command
}


def main():
	args = sys.argv[1:]  # skip call to jno from args list
	if len(args) == 0:
		print(Fore.RED + "No commands given" + Fore.RESET)
	else:
		command = args[0]
		try:
			jno_function = command_dict[command]
		except KeyError as e:
			print(Fore.RED + "ERROR: Command " + Fore.YELLOW + command + Fore.RED + " not found" + Fore.RESET)
		else:
			try:
				create_global_settings()
				jno_function(args[1:])  # skip command name from args list
			except JnoException as e:
				print(Fore.RED + "ERROR: {}".format(str(e)) + Fore.RESET)

if __name__ == '__main__':
	main()
