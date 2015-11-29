# smart-irrigation

## Installation

### Raspbian

See [here](https://www.raspberrypi.org/help/noobs-setup/) for information on installing Raspbian on a Raspberry Pi.

### Python

Python 2.7 or higher is required. For a Raspberry Pi running Raspbian, this should be installed by default. If it is not, follow the instructions for installation on Debian found [here](https://wiki.python.org/moin/BeginnersGuide/Download).

### MySQL

The project requires a MySQL database to function. Instructions for installing MySQL on a server can be found [here](https://dev.mysql.com/doc/refman/5.7/en/installing.html). Instructions for setting up MySQL with Amazon Web Services can be found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SettingUp.html).

### Python libraries for ReadSerial

The ReadSerial script depends on the MySQLdb and the py pyserial libraries. To install, run the commands

    sudo apt-get install python-dev libmysqlclient-dev
    pip install MySQL-python pyserial

The first line installs dependencies for the MySQL-python library.

### Python libraries for the API

The API comes with a requirements.txt file listing all of its dependencies. To easily install these dependencies, run the command

    pip install -r /path/to/requirements.txt

Depending on your server, you may also need to install the `python-dev` and `libmysqlclient-dev` packages in order to install the MySQL-python library. The following command will do that for you on a debian system.

    sudo apt-get install python-dev libmysqlclient-dev

## Running

### Creating a config file

The different components of this project rely on a config file which contains information on the location and login credentials of a MySQL server, the various fields to be read in from the hardware sensors, and a key for access to an external weather API.

To generate a template for this file, run ConfigGen.py.

Fill in the template with values specific to your implementation. An example config file is shown below.

    [MySQL]
    user = user_name
    password = password
    host = address_of_server.com
    database = database_name
    table = table_name

    [fields]
    time = TIMESTAMP
    s1 = INT
    s2 = INT
    s3 = INT
    temp = INT

    [weather]
    key = 165e1360651cd2e1

Each pair in the fields section corresponds to a column in the MySQL table. The name represents the name of the column and the value represents the datatype of the column.

### Generating test data

To generate test data, first create the file RandCSV.cfg and fill it with values specific to your project. An example is shown below.

    [Dates]
    time = '%Y-%m-%d %H:%M:%S'
    [Integers]
    s1 = 0,100
    s2 = 0,100
    s3 = 0,100
    temp = 20,120

This cfg file uses the same fields specified in the fields section of the config file. For date values, specify the format the date should be printed in. For integer values (such as most sensor readings) specify the range of values the sensors should return.

Once this file is created and filled with appropriate values, run RandCSV.py. It takes two arguments, the name of the output file and the number of entries to generate. For example, to create a csv file named test_input with 200 entries you would run the following command.

    python RandCSV.py test_input 200

### Pushing data to MySQL server

The script for reading data from input devices and pushing that data to the MySQL server is called ReadSerial.py. To run this script, first make sure that you have successfully created a config file as detailed above. Next, you will need to create one more configuration file called serial_devices.ini. An example serial_devices.ini is shown below:

    [devices]
    /dev/ttyUSB0=serial

    [format]
    /dev/ttyUSB0=s1,s2,s3,temp

    [table]
    /dev/ttyUSB0=entry

The devices contains paths to each device as keys, and either serial or some other value as values. If the value is serial, a serial connection will be opened to the provided path. Otherwise, stdin will be used for testing purposes.

The format section lists the names of the fields to be read in separated by commas.

The table section lists the MySQL table that the data from a device should be pushed to.

Once config and serial_devices.ini have been created, place them in the same directory as ReadSerial.py and then run the following command.

    python ReadSerial.py

NOTE: The current implementation assumes that the values read in will be tab separated, as they were in the original implementation of the data aggregators. In the future, it would be useful to allow for customizing the separation character.

NOTE: The current implementation uses 9600 baud for all serial connections. In the future, it would be useful to allow the baud rates to be configured for individual devices via serial_devices.ini.

NOTE: The current implementation relies on the two config files being in the same directory, and may also rely on the command being executed from within that directory. Ideally, future iterations should remove these requirements.

## Using the API

### get_field_between_time

Returns the entries for the specified field(s) and time from the given table between the given dates.

Arguments
* field: The name of the field to pull. Including this option multiple times allows you to pull multiple fields at once.
* start: The start time. The query will include all entries between the start time and the end time. Format: `\"%Y-%m-%d_%H:%M:%S\"`
* end  : The end time. The query will include all entries between the start time and the end time. Format: `\"%Y-%m-%d_%H:%M:%S\"`
* table: The table to pull from.

Example call:

    /get_field_between_time?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22&table=entry

This will pull the s1, s2 and time fields from the table entry. The start date is 2014-10-06_06:27:29 and the end date is 2015-12-22_14:04:29. The %22 is URL encoding for quote marks. The result is a JSON encoded list of dictionaries.

Example result:

    [
        {
            "s1": 16, 
            "s2": 33, 
            "time": "2014-10-06 06:27:29"
        }, 
        {
            "s1": 16, 
            "s2": 33, 
            "time": "2015-10-06 06:27:29"
        }, 
        {
            "s1": 63, 
            "s2": 57, 
            "time": "2015-11-02 09:21:05"
        }, 
        {
            "s1": 21, 
            "s2": 56, 
            "time": "2015-11-12 12:09:42"
        }, 
        {
            "s1": 99, 
            "s2": 21, 
            "time": "2015-12-21 07:13:15"
        }
    ]

### get_average

Returns the averages for the specified field(s) from the given table between the given dates.

Arguments
* field: The name of the field to pull. Including this option multiple times allows you to pull multiple fields at once.
* start: The start time. The query will include all entries between the start time and the end time. Format: `\"%Y-%m-%d_%H:%M:%S\"`
* end  : The end time. The query will include all entries between the start time and the end time. Format: `\"%Y-%m-%d_%H:%M:%S\"`
* table: The table to pull from.

Example call:

    /get_average?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22&table=entry

This will pull the averages of s1 and s2 from the table entry. The start date is 2014-10-06_06:27:29 and the end date is 2015-12-22_14:04:29. The %22 is URL encoding for quote marks.

Example result:

    [
        {
            "s1": 47.3, 
            "s2": 43.0
        }
    ]

### get_field_between_key

Returns the specified fields (including the key field) that fall in between the start and end condition of the key field.

Arguments
* field: The name of the field to pull. Including this option multiple times allows you to pull multiple fields at once.
* start: The start value. The query will include all entries with key between the start and end values.
* end  : The end value. The query will include all entries with key the start and end values.
* table: The table to pull from.
* key  : The field to compare to the start and end values.

Example call:

    /get_field_between_key?field=s1&field=s2&start=80&end=120&table=entry&key=temp

This will pull the values of s1, s2, and temp from the entry table from all entries where temperature is between 80 and 120.

Example result:

    [
        {
            "s1": 16, 
            "s2": 33, 
            "temp": 83
        }, 
        {
            "s1": 16, 
            "s2": 33, 
            "temp": 100
        }, 
        {
            "s1": 63, 
            "s2": 57, 
            "temp": 81
        }, 
        {
            "s1": 21, 
            "s2": 56, 
            "temp": 97
        }, 
        {
            "s1": 99, 
            "s2": 21, 
            "temp": 83
        }
    ]

### post_watering

Given a start date, a duration in minutes, a gallons per minute rating, and the name of a table (corresponding to a garden), this function will enter the date, duration and gallons per minute rating into a database and link this entry with readings from the given table. For debugging purposes it may return a JSON object containing the entries from the given table that fall into the range of the watering session, but this is not guaranteed.

Arguments
* start      : The start time. Format: `\"%Y-%m-%d_%H:%M:%S\"`
* duration   : The length of the watering session in minutes. Example: `60`
* gal_per_min: The gallons per minute rating of the garden. Example: `10.0`
* table      : The table to pull from.

Example call:

    /post_watering?start=%222015-10-06_06:27:29%22&duration=60&table=entry&gal_per_min=10.0

This will specify a start date of 2015-10-06_06:27:29, a duration of 60 minutes, a gallons per minute rating of 10, and the resulting database entry will be linked to entries in the table named entry.

No example result is given because the function is not guaranteed to return a result.