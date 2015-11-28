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

import csv
import sqlLib




with open('test_input', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    sqlLib.initConfig()
    sqlLib.connectDB()
    for row in reader:
        #print row
        sqlLib.pushData(row)

sqlLib.closeDB()