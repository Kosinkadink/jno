#!/usr/bin/python2
import sys, os, getopt, subprocess, shutil

# directory of arduino executable
# right click on file, click "Copy Path(s)"
arduino_exec = """/home/pi/Documents/arduino-1.8.0"""
arduino_exec_loc = os.path.join(arduino_exec,"arduino")
arduino_exec_libs = os.path.join(arduino_exec,"libraries")
arduino_script_loc = """/home/pi/Robotics-RPi-Arduino/Tunnel Robot/arduino/all_func_wheels/src/sketch/sketch.ino"""
arduino_port = "/dev/arduino_allfunc"
arduino_script_libs = """/home/pi/Robotics-RPi-Arduino/Tunnel Robot/arduino/all_func_wheels/lib"""


# Copy and replace all libs from script's lib folder
def move_libs():
	for item in os.listdir(arduino_script_libs):
		itempath = os.path.join(arduino_script_libs,item)
		if os.path.isdir(itempath):
			execpath = os.path.join(arduino_exec_libs,item)
			try:
				shutil.copytree(itempath,execpath)
			except OSError:
				shutil.rmtree(execpath)
				shutil.copytree(itempath,execpath)
			finally:
				print 'Copied lib {}'.format(item)
				

def main(argv):
	arg_list = [arduino_exec_loc]
	try:
		opts,args = getopt.getopt(argv, 'vup:b:',['verify=','upload=','port=','board='])
	except getopt.GetoptError:
		print 'invalid arguments'
		quit()
	for opt, arg in opts:
		if opt in ("-v","--verify"):
			arg_list.append("--verify")
			arg_list.append(arduino_script_loc)
		if opt in ("-u","--upload"):
			arg_list.append("--upload")
			arg_list.append(arduino_script_loc)
		if opt in ("-p","--port"):
			if arg.strip() == "":
				raise ValueError("no port provided")
			arg_list.append("--port")
			arg_list.append(arg)
		if opt in ("-b","--board"):
			if arg.strip() == "":
				raise ValueError("no board type provided")
			arg_list.append("--board")
			arg_list.append("arduino:avr:"+arg.strip())
	if len(arg_list) < 2:
		print "no arguments received, doing nothing..."
	else:
		if "--upload" in arg_list and "--port" not in arg_list:
			arg_list.append("--port")
			arg_list.append(arduino_port)
		#add particular board, uncomment the correct one
		if "--board" not in arg_list:
			arg_list.append("--board")
			arg_list.append("arduino:avr:mega")
		##### arg_list.append("arduino:avr:uno")
		
		print arg_list
		
		#decide if to move libraries over
		if "--upload" in arg_list or "--verify" in arg_list:
			move_libs()
		
		os.system('cd ~')
		subprocess.check_call(arg_list)
		print 'ALL ACTIONS COMPLETED'


if __name__ == '__main__':
	main(sys.argv[1:])
