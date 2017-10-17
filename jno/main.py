#!/usr/bin/python2
import sys
import os
from colorama import init, Fore

import jno.commands
from jno.commands.setdefault import SetDefault
from jno.commands.init import Init
from jno.commands.jnoserial import JnoSerial
from jno.commands.build import Build
from jno.commands.upload import Upload
from jno.commands.listmodels import ListModels
from jno.commands.clean import Clean
from jno.util import JnoException

# directory from which this script is ran
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))
if os.name == 'nt':
	__location__ = __location__.replace('\\','/')
	init()


DEBUG = False


def init_command(argv):
	Init(argv,os.getcwd())

def build_command(argv):
	Build(argv,__location__)

def upload_command(argv):
	Upload(argv,__location__)

def serial_command(argv):
	JnoSerial(argv,__location__)

def setglobal_command(argv):
	SetDefault(argv,__location__)

def setlocal_command(argv):
	SetDefault(argv,os.getcwd())

def listmodels_command(argv):
	ListModels(argv,__location__)

def clean_command(argv):
	Clean(argv,__location__)


# Dictionary linking option to function
command_dict = {
	"init": init_command,
	"build": build_command,
	"upload": upload_command,
	"serial": serial_command,
	"setglobal": setglobal_command,
	"setlocal": setlocal_command,
	"listmodels": listmodels_command,
	"clean": clean_command
}


def main():
	args = sys.argv[1:]
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
				jno_function(args)
			except JnoException as e:
				print(Fore.RED + "ERROR: {}".format(str(e)) + Fore.RESET)

if __name__ == '__main__':
	main()
