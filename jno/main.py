#!/usr/bin/python2
import sys
import os

import jno.commands
from jno.commands.setdefault import SetDefault
from jno.commands.init import Init
from jno.commands.jnoserial import JnoSerial
from jno.commands.build import Build
from jno.commands.upload import Upload
from jno.util import JnoException

# directory from which this script is ran
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))
if os.name == 'nt':
	__location__ = __location__.replace('\\','/')


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


# Dictionary linking option to function
command_dict = {
	"init": init_command,
	"build": build_command,
	"upload": upload_command,
	"serial": serial_command,
	"setglobal": setglobal_command,
	"setlocal": setlocal_command
}


def main():
	args = sys.argv[1:]
	if len(args) == 0:
		print "No commands given"
	else:
		command = args[0]
		try:
			jno_function = command_dict[command]
		except KeyError,e:
			print "ERROR: Command {} not found".format(command)
		else:
			try:
				jno_function(args)
			except JnoException,e:
				print 'ERROR: {}'.format(str(e))

if __name__ == '__main__':
	main()
