from jno.util import interpret_configs
from jno.commands.command import Command

import os
import serial.tools.list_ports
from colorama import Fore

class Ports(Command):

	def run(self,argv,__location__):
		jno_dict = interpret_configs()
		ports = serial.tools.list_ports.comports()
		for port in ports:
			print(port)
			print("{},{},{},{},{},{},{},{},{},{},{}".format(
				port.device,
				port.name,
				port.description,
				port.hwid,
				port.vid,
				port.pid,
				port.serial_number,
				port.location,
				port.manufacturer,
				port.product,
				port.interface))
		