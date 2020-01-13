from jno.util import interpret_configs
from jno.util import get_all_ports
from jno.util import JnoException
from jno.commands.command import Command

import os
import getopt
from sys import version_info
from colorama import Fore

class Ports(Command):

	help_name = "Ports"
	help_usage = "jno ports [-p, --port=] portname"
	help_description = "Without arguments, prints list of all detected ports. With -p, prints details about specific port."

	def run(self,argv,location):
		jno_dict = interpret_configs()
		ports = get_all_ports()
		self.perform_ports(argv,ports)
	
	def perform_ports(self,argv,ports):
		if not ports:
			print("{}No ports detected{}".format(Fore.YELLOW,Fore.RESET))
			return
		try:
			opts,args = getopt.getopt(argv, 'p:', ['port='])
		except getopt.GetoptError as e:
			raise JnoException(str(e))
		# if a board is provided, show info about it
		for opt, arg in opts:
			if opt in ("-p","--port"):
				return self.print_port_data(arg,ports)
		# otherwise, list all models
		self.print_all_ports(ports)

	def print_all_ports(self,ports):
		print(Fore.CYAN+"======================")
		print("{2}{0}{3} :: {4}{1}{3}".format("Port","Description",Fore.YELLOW,Fore.CYAN,Fore.MAGENTA))
		print("----------------------")
		for port in ports:
			print("{2}{0}{3} :: {4}{1}{3}".format(port.device,port.description,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA))
		print("======================"+Fore.RESET)

	def print_port_data(self,device,ports):
		# see if port exists
		relevant_port = None
		for port in ports:
			if port.device == device:
				relevant_port = port
				break
		if not relevant_port:
			raise JnoException("port '{}' is not recognized".format(device))
		properties = {
						"Name": relevant_port.name,
						"HWID": relevant_port.hwid,
						"VID": relevant_port.vid,
						"PID": relevant_port.pid,
						"Serial Number": relevant_port.serial_number,
						"Location": relevant_port.location,
						"Manufacturer": relevant_port.manufacturer,
						"Product": relevant_port.product,
						"Interface": relevant_port.interface
					 }
		print(Fore.CYAN+"======================")
		print("Port: {2}{0}{3} ({1}){4}".format(relevant_port.device,relevant_port.description,Fore.GREEN,Fore.MAGENTA,Fore.CYAN))
		if version_info < (3,0): # python2 code
			for name,value in properties.iteritems():
				self.print_property_with_value(name,value)
		else: # python3 code
			for name,value in properties.items():
				self.print_property_with_value(name,value)
		print("======================"+Fore.RESET)

	def print_property_with_value(self,name,value):
		# if there's a value, print it
		if value:
			print("  {3}{0}: {2}{1}{3}".format(name,value,Fore.YELLOW,Fore.CYAN))
