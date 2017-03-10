from jno.util import interpret_configs
from jno.commands.command import Command

import getopt
import serial
import threading
import sys


# class used for serial communication
class JnoSerial(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs(__location__)
		jno_dict = self.parse_serial_args(argv[1:],jno_dict)
		self.start_serialcomm(jno_dict)


	# Parse arguments passed into JnoSerial
	def parse_serial_args(self,argv,jno_dict):
		try:
			opts,args = getopt.getopt(argv, 'p:b:',['port=','baud='])
		except getopt.GetoptError:
			print 'invalid arguments'
			quit()
		for opt, arg in opts:
			if opt in ("-p","--port"):
				if arg.strip() == "":
					raise ValueError("no port provided")
				jno_dict["PORT"] = arg
			elif opt in ("-b","--baud"):
				if arg.strip() == "":
					raise ValueError("no baudrate provided")
				jno_dict["BAUDRATE"] = arg
		return jno_dict


	# Open serial communication with arduino
	def start_serialcomm(self,jno_dict):
		PORT = jno_dict["PORT"]
		
		try:
			BAUD = int(jno_dict["BAUDRATE"])
			ard_serial = serial.Serial(PORT, BAUD)
		except ValueError,e:
			print str(e)
			return
		except Exception,e:
			print str(e)
			return
			
		if ard_serial.isOpen():
			ard_serial.close()
			ard_serial.open()

		print ':: successfully started serial'
		print ':: port: {}'.format(PORT)
		print ':: baudrate: {}'.format(BAUD)
		print ':: type EXIT to leave serial'
		print ''
		# create thread for receiving serial stuff
		ser_event = threading.Event()
		ser_message_sent = threading.Event()
		ser_thread = threading.Thread(target=self.serial_function,args=(ard_serial,ser_event,ser_message_sent))
		ser_thread.daemon = True
		ser_thread.start()
		# echo user input to the serial device
		while True:
			user_inp = raw_input()
			ser_message_sent.set()
			if user_inp.strip() == "EXIT":
				break
			else:
				ard_serial.write(user_inp.strip())
		ser_event.set()


	# Function ran in another thread to read serial input
	def serial_function(self,ard_serial,ser_event,ser_message_sent):
		ard_serial.timeout = 0.1
		while not ser_event.is_set():
			recvd = ard_serial.read()
			sys.stdout.write(recvd)
			if not ser_message_sent.is_set() and recvd:
				print ""


	# Return first working serial connection
	def get_first_serial(self,baud):
		for num in range(0,5):
			pass


	# Try to start serial comm with device
	def get_serial_comm(self,port,baud):
		pass
