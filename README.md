# jno
Command line interface wrapper for Arduino IDE, inspired by ino.

# Installation
Using PyPi, the package can be obtained using:
	
	pip install jno
	
Or you can download the repo and use:

	pip install .

# Initialize
To begin using jno, change working directory to your project. Then, perform:

	jno init

This will initialize the basic directory structure and create a *jno.jno* file, which stores the local jno settings.

Note that on Windows, calling jno like this may not work. Instead, call the jno module directly:

	python -m jno

By default, jno does not know where your Arduino IDE is located - this is represented by exec_dir in the config. There is a local and a global version of *jno.jno* files. The local *jno.jno* file overwrites the global version IF the parameters are not set to NULL or DEFAULT. To set up your exec_dir, find your Arduino folder - say /home/pi/Documents/arduino-1.8.10. Perform:

	jno setglobal --exec_dir=/home/pi/Documents/arduino-1.8.10
	
OR

	jno setlocal --exec_dir=/home/pi/Documents/arduino-1.8.10

depending on what you plan on doing - setglobal means a local .jno with exec_dir set to NULL will use the global exec_dir instead.

Once exec_dir is set, jno is ready to go. You should change the global and local settings to your liking - the options are documented below. Global settings are stored in the local user's home folder in a *.jnoglobal.jno* file.

# Usage
The commands supported are:

*jno build [parameters]*: compile the code, verifying that there are no errors

*jno upload [parameters]*: compile + upload the code

*jno serial [parameters]*: start a serial monitor

*jno init*: initialize current working directory with libraries/, sketch/, and *jno.jno* if they are not present

*jno clean*: removes all build files (located in .build of directory)

*jno boards [optional parameters]*: list the board models supported by your Arduino IDE

*jno ports [optional parameters]*: list the ports currently available

*jno setlocal [setting]*: change setting in local *jno.jno*

*jno setglobal [setting]*: change setting in global *jno.jno*

*jno help [command name]*: lists usage and description for all commands, or for a specific command

## Settings (for setlocal and setglobal)
These settings are the same as those contained in *jno.jno* files. These settings WILL be saved locally or globally. Note that lower case inputs are equally as valid. Possible parameters are as follows:

*--exec_dir=/some/dir*: directory that contains the arduino executable file. NULL is the default value.

*--board=boardname*: board that code should be compiled for. Possible 'boardname' choices include *uno* and *mega*. For boardname options, use the *boards* command.

*--port=/some/port*: port of arduino to upload code or start serial communication. On Linux, dmesg is useful in determining this.

*--baudrate=9600*: baudrate used for serial communication. Must be an integer.

*--sketch_dir=/some/dir*: directory of the local jno 'home'. Only mess with this if this *jno.jno* is meant to point to a deeper directory.

## Parameters (for other commands)
Parameters are used only for the current invocation of the command and override local settings - they WILL NOT be saved. Possible settings are:

*-p, --port=/some/port*: see --port above. Affects the upload, serial, and ports commands.

*-b, --board=boardname*: see --board above. Affects the build, upload, and boards commands.

*-b, --baudrate=9600*: see --baudrate above. Only affects serial command.

*-e, --endline=some_string*: adds string on to end of any sent serial message. Only affects serial command.

*-q, --quit=some_string*: sets string that quits serial when entered ('EXIT' by default). Only affects serial command.

*-n, --noreplace*: turns off replacement of \n or \r in user-sent data with newline or carriage return. Only affects serial command.

Note: invoking any command with "help" following the command name will print the help string for the command instead, as if *jno help [command name]* was invoked.

# jno Directory Structure

 A valid jno directory contains a *libraries* directory, a *sketch* directory with a *sketch.ino* inside, and a *jno.jno* file. The *libraries* directory should contain any libraries not included in your Arduino IDE. The structure looks like this:

```
my_ard_proj
    .
    |-- jno.jno           [configuration file]
    |-- libraries         [directory containing dependencies]
    |-- sketch            [directory containing main program .ino file]
    |   `-- sketch.ino
    |
    `-- .build            [directory for build files]
```

# References

This tool is a wrapper for the Arduino IDE commandline interface, documented here:
https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
