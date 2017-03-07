# jno
Command line interface wrapper for Arduino IDE, inspired by ino.

# Usage
Place jno script into a folder (by default, expects to be in same directory as sketch/sketch.ino).

Execute with either

	python jno [options]
	
OR 
	
	chmod -x jno (only need to add execution perm once)
	./jno [options]

# Initialize
To initialize directories and .jno file, perform

	./jno init
	
Modify the created *jno.jno* file to fit your needs. Note that all paths must be absolute, except for SCRIPT_DIR if the directory does not begin with /

* EXEC_DIR is the directory of your Arduino IDE. For example, */home/pi/Documents/arduino-1.8.1*

* EXEC_LIBS with the DEFAULT option is the EXEC_DIR + libraries

* BOARD specifies the hardware the code should be compiled for. Examples include *arduino:avr:uno* and *arduino:avr:mega*

* BAUDRATE chooses baudrate for serial communication

* SKETCH_DIR is the directory that contains the libraries and sketch folder. Structure is as follows:

```
.
|-- lib         [directory containing dependencies]
|
|-- sketch
|   `-- sketch.ino
|
|-- jno         [this script]
`-- jno.jno
```

# Actions
*./jno build (or -v) [parameters]*: compile the code

*./jno upload (or -u) [parameters]*: compile + upload the code

*./jno serial [parameters]*: start serial communication with arduino

## Parameters
*--board [board]*: choose board

*--port (or -p) [port]*: choose port

*--baud (or -b) [baudrate]*: choose baudrate for serial communication

