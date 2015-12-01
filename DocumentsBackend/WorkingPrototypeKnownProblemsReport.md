% Working Prototype Known Problems Report
% Theodore Handleman; Coy Humphrey; Ernesto Hernandez; Ryan Connors; Ryan Fulscher
% November 30, 2015

# Functions not working correctly by component

## API

* Incorrect values in config file will cause program to break

## Library

* Some functions are not used by other files, and have not been re-tested since code change
	* Functions guaranteed to work
		* initConfig(), initCheck(), pushData(), connectDB(), executeCommand(), closeDB()
	* Untested functions
		* showTables(), selectCol(), createTable(), clearRows(), addSensorCol()
* Relies on the config file being in the same directory as the program is called from
	* If it is not, then the program will not be able to find the config file and will break

* Assumes MySQL values in config file are correct and will break if they are not or if they are missing

## ReadSerial

* Does not check for errors in input
	* Incorrect values in config files will cause the program to break
	* Incorrect values read from USB devices or stdin will cause the program to break
* USB functionality unable to be tested
	* Our sponsor has still not gotten the hardware sensors to work, so we cannot test our code with a USB connection.
	* Instead we have used stdin and emulated the output of the USB devices that will be used in the future.
* Relies on the config file being in the same directory as the program is called from
	* If it is not, then the program will not be able to find the config file and will break

## Prototypes

The files found in the Prototypes directory are quick and dirty scripts made to test certain features. None of them are guaranteed to work, and many are buggy. They are not used for anything anymore and are kept only to preserve history.