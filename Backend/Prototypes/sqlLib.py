#sqlDynamicsRows.py is a script that is evolving into a function library for python to access a Database.
# UNTESTED DO NOT RUN ME
# UNTESTED DO NOT RUN ME
# This was written for python, but on a lab computer without a python environment. Testing will commence at home later.
# So nothing has actually be run yet and is probably full of little errors.

import ConfigParser
import mysql.connector
import os
import subprocess
import sys
from time import time
from datetime import datetime


config = None
sql_config = None

context = None
cursor = None
activeTable = None
colFormat = []

def closeDB ( ) :
	cursor.close( )
	context.close( )
	
def initCheck ( ) :
	if activeTable == None :
		print "pushData( ) called with undefined activeTable"
		sys.exit( )
	elif cursor == None :
		print "pushData( ) called with undefined cursor"
		sys.exit( )

def executeCommand (command) :
	global cursor
	global context
	
	cursor.execute(command)
	print cursor.fetchwarnings( )	
	context.commit( )
	
def clearRows ( ) :
	global cursor
	global context
	global activeTable
	
	initCheck( )
	
	command = "TRUNCATE TABLE %s" % activeTable
	executeCommand( command )

#push Data pushes a set of data contained in the list structure senseData to the SQL DB
#pushData accepts time as a string, sensorList as a list of sensor readings, and temp as an integer or double
#preconditions, colFormat is defined, Cursor is connected and nonnull, activeTable is nonnull
def pushData ( time, sensorList, temp ) :
	global activeTable
	global colFormat
	global cursor
	
	#ensure precons are met and cardinality of input data matches col set.
	initCheck ( )
	if len(sensorList)+2 != len(colFormat) :
		print "pushData( ) called with data that does not match col format."
		sys.exit( )
	
	jDelim = ', '
	#create dictionary representative of data entry
	addEntry = "INSERT INTO " + activeTable + "("
	addEntry += jDelim.join(colFormat) + ") VALUES (\"%s\", " % (time)
	addEntry += jDelim.join(str(reading) for reading in sensorList) + ", %d" % (temp)
	addEntry += ")"
	
	executeCommand( addEntry )
	
	
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
	
#current test
colFormat = ["time", "s1", "s2", "s3", "temp"]	

initConfig( )
connectDB( )
pushData( '1988-10-06 06:27:24', [50, 50, 50], 67)
closeDB( )
