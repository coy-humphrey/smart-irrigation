#!/usr/bin/python

'''
A tool to generate an example config file
'''
import ConfigParser

config = ConfigParser.RawConfigParser()
# Create section containing MySQL data
config.add_section('MySQL')
# Username and password for MySQL server
config.set('MySQL', 'user', 'smart_irrigation')
config.set('MySQL', 'password', '3Kv32B8JEliX0Qhk')
# Address of server
config.set('MySQL', 'host', 'smart-irrigation.canqqif3vrwd.us-west-1.rds.amazonaws.com')
# Name of database and table containing smart irrigation information
config.set('MySQL', 'database', 'smart_irrigation')
config.set('MySQL', 'table', 'entry')

# Section containing all the fields that we will store in the database
# Will be in format "fieldname = SQL Data Type"
config.add_section('fields')
config.set('fields', 'time', 'TIMESTAMP')
config.set('fields', 'moisture_sensor_1', 'DOUBLE')

# Writing our configuration file to 'example.cfg'
with open('config', 'wb') as configfile:
    config.write(configfile)