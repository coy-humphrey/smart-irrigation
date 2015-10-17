#!/usr/bin/python

'''
Proof of concept, showing how to read from a config file, and
connect to a MySQL database in python.

Future goals:
* Use fields section of config file to initialize a table with the given
  fields, or alter an existing table to have all of the given fields
* Read data from Serial using fields section of config file to determine
  type and order of data received. Write this data to database.
'''

import ConfigParser
import mysql.connector

# Initialize our ConfigParser to read the config file
config = ConfigParser.RawConfigParser()
config.read('config')

# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'password': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'database': config.get('MySQL', 'database'),
  'raise_on_warnings': True,
}
table = config.get ('MySQL', 'table')

# Print settings for debugging purposes
print sql_config

# Attempt to connect to the MySQL server, spit out an error on failure
try:
  cnx = mysql.connector.connect(**sql_config)
except mysql.connector.Error as err:
  if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
# Disconnect from server if we successfully connected
# This would be where we put code that actually does something with the
# database we've opened
else:
  # Download warnings and errors after executing commands
  cnx.get_warnings = True
  cursor = cnx.cursor()
  # Use some Python string manipulation to set up command
  # This will add the entries from the below dictionary into a row
  add_entry = ("INSERT INTO " + table + " "
                "(time, s1, s2, s3, temp) "
                "VALUES (%(time)s, %(s_one)s, %(s_two)s, %(s_three)s, %(temp)s)")
  # Dictionary holding the values to add.
  # For now they are hard coded, but when we start actually pulling information
  # from a serial connection, we will store that information here
  data_entry = {
    'time': '2015-10-06 06:27:23',
    's_one'  : '16',
    's_two'  : '33',
    's_three'  : '9',
    'temp': '67',
  }
  # Execute the command, fetch and print any warnings, then commit changes
  cursor.execute(add_entry, data_entry)
  print cursor.fetchwarnings()
  cnx.commit()
  # Cleanup
  cursor.close()
  cnx.close()