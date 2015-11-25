#!/usr/bin/python

'''
A tool to generate an example config file
'''
import ConfigParser

config = ConfigParser.RawConfigParser()
# Create section containing MySQL data
config.add_section('MySQL')
# Username and password for MySQL server
config.set('MySQL', 'user', 'user_name')
config.set('MySQL', 'password', 'password')
# Address of server
config.set('MySQL', 'host', 'address_of_server.com')
# Name of database and table containing smart irrigation information
config.set('MySQL', 'database', 'database_name')
config.set('MySQL', 'table', 'table_name')

# Section containing all the fields that we will store in the database
# Will be in format "fieldname = SQL Data Type"
config.add_section('fields')
config.set('fields', 'time_field', 'TIMESTAMP')
config.set('fields', 'integer_field', 'INT')

config.add_section('weather')
config.set('weather','key','copy_key_here')

# Writing our configuration file to 'example.cfg'
with open('config', 'wb') as configfile:
    config.write(configfile)