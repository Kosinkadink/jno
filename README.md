# jno
Command line interface wrapper for Arduino IDE, inspired by ino.

# Installation
Using PyPi, the package can be obtained using:
	
	pip install jno

If you prefer running the setup.py, then download repo, change working directory and do:

	make install

# Initialize
To begin using jno, change working directory to your project. Then, perform:

	jno init

This will initialize the basic directory structure and create a *jno.jno* file, which stores the local jno settings.

By default, jno does not know where your Arduino IDE is located - this is represented by EXEC_DIR in the config. There is a local and a global version of *jno.jno* files. The local *jno.jno* file overwrites the global version IF the parameters are not set to NULL or DEFAULT. To set up your EXEC_DIR, find your Arduino folder - say /home/pi/Documents/arduino-1.8.1. Perform:

	jno setglobal --EXEC_DIR=/home/pi/Documents/arduino-1.8.1
	
OR

	jno setlocal --EXEC_DIR=/home/pi/Documents/arduino-1.8.1

depending on what you plan on doing - setglobal means a local .jno with EXEC_DIR set to NULL will use the global EXEC_DIR instead.

Once EXEC_DIR is set, jno is ready to go. You should change the global and local settings to your liking - the options are documented below.

# Usage
The commands supported are:

*jno build [parameters]*: compile the code, verifying that there are no errors

*jno upload [parameters]*: compile + upload the code

*jno serial [parameters]*: start a serial monitor

*jno init*: initialize current working directory with lib/, sketch/, and *jno.jno* if they are not present

*jno listmodels*: list the board models supported by your Arduino IDE

*jno setlocal [setting]*: change setting in local *jno.jno*

*jno setglobal [setting]*: change setting in global *jno.jno*

## Settings (for setlocal and setglobal)
These settings are the same as those contained in *jno.jno* files. These settings WILL be saved locally or globally. Note that lower case inputs are equally as valid. Possible parameters are as follows:

*--EXEC_DIR=/some/dir*: directory that contains the arduino executable file. NULL is the default value.

*--EXEC_LIBS=/some/dir/libraries*: directory that Arduino IDE loads libraries from. By DEFAULT, this uses arduino's internal libraries/ directory, but this may be unsafe if your local lib/ contents have the same name as core libraries.

*--BOARD=boardname*: board that code should be compiled for. Possible 'boardname' choices include *uno* and *mega*. For boardname options, use the *listmodels* command.

*--PORT=/some/port*: port of arduino to upload code or start serial communication. On Linux, dmesg is useful in determing this.

*--BAUDRATE=9600*: baudrate used for serial communication. Must be an integer.

*--SKETCH_DIR=/some/dir*: directory of the local jno 'home'. Only mess with this if this *jno.jno* is meant to point to a deeper directory.

## Parameters (for other commands)
Parameters are used only for the current invocation of the command and override local settings - they WILL NOT be saved. Possible settings are:

*-b, --baud=9600*: see --BAUDRATE above. Only affects serial command.

*-p, --port=/some/port*: see --PORT above. Affects the upload and serial commands.

*--board=boardname*: see --BOARD above. Affects the build and upload commands.

# jno Directory Structure

 A valid jno directory contains a *lib* directory, a *sketch* directory with a *sketch.ino* inside, and a *jno.jno* file. The *lib* directory should contain any libraries not included in your Arduino IDE. The structure looks like this:

```
my_ard_proj
    .
    |-- lib         [directory containing dependencies]
    |
    |-- sketch
    |   `-- sketch.ino
    |
    `-- jno.jno
```
