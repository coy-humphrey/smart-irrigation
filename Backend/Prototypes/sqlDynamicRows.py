#sqlDynamicsRows.py is a script that is evolving into a function library for python to access a Database.
# UNTESTED DO NOT RUN ME
# UNTESTED DO NOT RUN ME
# This was written for python, but on a lab computer without a python environment. Testing will commence at home later.
# So nothing has actually be run yet and is probably full of little errors.

import ConfigParse
import mysql.connector
import os
import subprocess
from time import time
from datetime import datetime


config = None
sql_config = None

context = None
cursor = None
activeTable = None

def closeDB ( ) :
	cursor.close( )
	context.close( )


#push Data pushes a set of data contained in the list structure senseData to the SQL DB
def pushData ( time, senseList,  temp) :
	#Template, fill in later
	return

#addCol will add a col to the active DB
def addSensorCol ( colName ) :
	global activeTable
	
	#add check for valid table data-types 
	
	newCommand = ("ALTER TABLE " + activeTable + "ADD " + colName + " INT AFTER time")
	cursor.execute(newCommand)
	print cursor.fetchwarnings( )
	context.commit( )
	
#initConfig parse the config information into sql_config, if a config file is 
#not available it will create a new one if possible. If the creation process fails, the program will terminate with error.
#Preconditions : None
#Postconditions : config stores parsed config file, sql_config stores connection and account information.
def initConfig ( ) :
	
	global sql_config
	global config
	global activeTable

	if not os.path.isfile( 'config' ) :
		#attempt to generate config if it doesn't exist
		try :
			subprocess.check_call( "python ConfigGen.py" ,shell=True )
		except :
			print "config file could not be located, or created."
			sys.exit( )
	
	#config file located
	config = ConfigParser.RawConfigParser( )
	config.read( 'config' )
	
	sql_config = {
		'user': config.get('MySQL', 'user'),
		'password': config.get('MySQL', 'password'),
		'host': config.get('MySQL', 'host'),
		'database': config.get('MySQL', 'database'),
		'raise_on_warnings': True,	
	}
	
	activeTable = config.get('MySQL', 'table')

#connectDB will use the initialized sql_config data to connect to the database and 
#initialize the cursor and context variables.
#Preconditions : sql_config is properly initialized
#postconditions : context is tied to the active sql connection, cursor is in proper initial state.
def connectDB ( ) :
	global sql_config
	global context
	global cursor
	
	if sql_config == None :
		print "sqlDynamicRows.py : connectDB( ) was called without sql_config initialization\n"
		sys.exit( )
	#attempt connection and tie to context
	
	try:
	  context = mysql.connector.connect(**sql_config)
	except mysql.connector.Error as err:
	  if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password\n")
	  elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist\n")
	  else:
		print(err)
	
	#set context state machine to record errors and warnings
	context.get_warnings = True
	
	#set initial cursor position
	cursor = context.cursor( )
	
	
	
