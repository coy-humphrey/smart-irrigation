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
import csv
from time import time
from datetime import datetime


# Initialize our ConfigParser to read the config file
config = ConfigParser.RawConfigParser()
config.read('config')

# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'password': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'database': config.get('MySQL', 'database'),
  'raise_on_warnings': False,
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
# Successfully connected, now we can insert things
else:
  # Download warnings and errors after executing commands
  cnx.get_warnings = True
  cursor = cnx.cursor()
  # Use some Python string manipulation to set up command based on fields in config file
  # This will add the entries from the below dictionary into a row
  add_entry = ("INSERT INTO " + table + " "
                "(" + ",".join(config.options("fields")) + ") "
                "VALUES (" + ", ".join (map(lambda x: "%(" + x + ")s", config.options("fields"))) + ")")
  
  # Open csv file, read each row and use the created dictionary to make SQL command
  # This assumes that the csv file has identical fields to those listed in config file
  with open('test_input', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      cursor.execute(add_entry, row)
      print cursor.fetchwarnings()
  # Commit changes
  cnx.commit()
  
  # Cleanup
  cursor.close()
  cnx.close()