# jno
Command line interface wrapper for Arduino IDE, inspired by ino

# Usage
Place jno script into a folder (by default, expects to be in same directory as sketch/sketch.ino).

Execute with either 'python jno <options>', or './jno <options>' after 'chmod -x jno'.

To initialize directories and .jno file, perform

	./jno --init
	
Modify the created jno.jno file to fit your needs.

EXEC_DIR is the directory of your Arduino IDE.

EXEC_LIBS with the DEFAULT option is the EXEC_DIR + libraries/

All paths must be absolute, except for SCRIPT_DIR if '/' is used alone.
