#!/usr/bin/python

'''
A tool to generate an example config file
'''
import ConfigParser

config = ConfigParser.RawConfigParser()
# Create section containing MySQL data
config.add_section('MySQL')
# Username and password for MySQL server
config.set('MySQL', 'user', 'username')
config.set('MySQL', 'password', 'password')
# Address of server
config.set('MySQL', 'host', '127.0.0.1')
# Name of database and table containing smart irrigation information
config.set('MySQL', 'database', 'database_name')
config.set('MySQL', 'table', 'table_name')

# Section containing all the fields that we will store in the database
# Will be in format "fieldname = SQL Data Type"
config.add_section('fields')
config.set('fields', 'time', 'TIMESTAMP')
config.set('fields', 'moisture_sensor_1', 'DOUBLE')

# Writing our configuration file to 'example.cfg'
with open('config', 'wb') as configfile:
    config.write(configfile)