from jno.util import interpret_configs
from jno.util import verify_and_get_port
from jno.util import JnoException
from jno.commands.command import Command

import getopt
import serial
import threading
import sys
from sys import version_info
from colorama import Fore, Back


# class used for serial communication
class JnoSerial(Command):

	help_name = "Serial"
	help_usage = "jno serial [-p, --port=] port [-b, --baudrate] baudrate [-q, --quit=] 'quit_string' [-e, --endline=] 'ending_chars' [-n, --noreplace]"
	help_description = "Attempts to start serial communication with port. Without arguments, uses port/baudrate defined locally/globally. " \
		"By default, the quit string is 'EXIT'; use -q to change. By default, there are no characters added onto sent data; use -e " \
		"to specify ending characters to add. For the ending chars, any instances of '\\n' or '\\r' will be treated as newline or carriage return, respectively. " \
		"By default, any instances of '\\n' or '\\r' sent via user input to device will be treated as special characters, but using -n will deactivate " \
		"that functionality."

	def run(self,argv,location):
		jno_dict = interpret_configs()
		jno_dict = self.parse_serial_args(argv,jno_dict)
		self.start_serialcomm(jno_dict)

	# Parse arguments passed into JnoSerial
	def parse_serial_args(self,argv,jno_dict):
		try:
			opts,args = getopt.getopt(argv, "p:b:q:e:n",["port=","baudrate=","quit=","endline=","noreplace"])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		jno_dict["REPLACE"] = True
		for opt, arg in opts:
			if opt in ("-p","--port"):
				if arg.strip() == "":
					raise ValueError("no port provided")
				jno_dict["port"] = arg
			elif opt in ("-b","--baudrate"):
				if arg.strip() == "":
					raise ValueError("no baudrate provided")
				jno_dict["baudrate"] = arg
			elif opt in ("-q","--quit"):
				if arg.strip() == "":
					raise ValueError("no quit string provided")
				jno_dict["QUIT"] = arg
			elif opt in ("-e","--endline"):
				if arg.strip() == "":
					raise ValueError("no endline string provided")
				jno_dict["ENDLINE"] = arg
			elif opt in ("-n","--noreplace"):
				jno_dict["REPLACE"] = False
		return jno_dict


	# Open serial communication with arduino
	def start_serialcomm(self,jno_dict):
		# verify port or get first available
		port = verify_and_get_port(jno_dict["port"])
		if not port:
			if jno_dict["port"] == "DEFAULT":
				raise JnoException("no ports available")
			raise JnoException("port does not exist: {}".format(jno_dict["port"]))
		else:
			if jno_dict["port"] == "DEFAULT":
				print("{1}No port provided, using available port {0}{2}".format(port,Fore.YELLOW,Fore.RESET))

		if "QUIT" not in jno_dict:
			jno_dict["QUIT"] = "EXIT"
		if "ENDLINE" not in jno_dict:
			jno_dict["ENDLINE"] = ""
			endline_print = Fore.CYAN+"None"
		else:
			endline_str = jno_dict["ENDLINE"]
			endline_print = endline_str
			if "\\r" in endline_str:
				endline_str = endline_str.replace("\\r","\r")
				endline_print = endline_print.replace("\\r","{}\\r{}".format(Back.MAGENTA,Back.RESET))
			if "\\n" in endline_str:
				endline_str = endline_str.replace("\\n","\n")
				endline_print = endline_print.replace("\\n","{}\\n{}".format(Back.MAGENTA,Back.RESET))
			jno_dict["ENDLINE"] = endline_str

		try:
			baud = int(jno_dict["baudrate"])
			ard_serial = serial.Serial(port, baud)
		except ValueError as e:
			raise JnoException(str(e))
		except Exception as e:
			raise JnoException(str(e))
			
		if ard_serial.isOpen():
			ard_serial.close()
			ard_serial.open()

		print(Fore.CYAN + ":: successfully started serial")
		print(":: port: {1}{0}{2}".format(port,Fore.YELLOW,Fore.CYAN))
		print(":: baudrate: {1}{0}{2}".format(baud,Fore.YELLOW,Fore.CYAN))
		print(":: endline: {1}{0}{2}".format(endline_print,Fore.YELLOW,Fore.CYAN))
		print(":: type {1}{0}{2} to leave serial".format(jno_dict["QUIT"],Fore.YELLOW,Fore.CYAN))
		print("" + Fore.RESET)
		# create thread for receiving serial stuff
		ser_event = threading.Event()
		ser_message_sent = threading.Event()
		ser_thread = threading.Thread(target=self.serial_function,args=(ard_serial,ser_event,ser_message_sent))
		ser_thread.daemon = True
		ser_thread.start()
		# echo user input to the serial device
		while True:
			if version_info < (3,0): # python2 code
				user_inp = raw_input()
			else: # python3 code
				user_inp = input()
			ser_message_sent.set()
			if user_inp.strip() == jno_dict["QUIT"]:
				break
			else:
				user_inp = user_inp.strip()
				if jno_dict["REPLACE"]:
					# replace typed in \r and \n with carriage return or newline, respectively
					if "\\r" in user_inp:
						user_inp = user_inp.replace("\\r","\r")
					if "\\n" in user_inp:
						user_inp = user_inp.replace("\\n","\n")
				ard_serial.write(user_inp.encode()+jno_dict["ENDLINE"].encode())
		ser_event.set()
		ser_thread.join(timeout=2)


	# Function ran in another thread to read serial input
	def serial_function(self,ard_serial,ser_event,ser_message_sent):
		ard_serial.timeout = 0.1
		sys.stdout.flush()
		while not ser_event.is_set():
			recvd = ard_serial.read()
			sys.stdout.write(Fore.MAGENTA+recvd.decode()+Fore.RESET)
			if not ser_message_sent.is_set() and recvd:
				print("")
				ser_message_sent.set()
