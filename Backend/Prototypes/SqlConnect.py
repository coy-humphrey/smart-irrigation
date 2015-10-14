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
  cnx.close()