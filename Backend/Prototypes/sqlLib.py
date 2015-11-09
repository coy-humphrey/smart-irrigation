#sqlDynamicsRows.py is a script that is evolving into a function library for python to access a Database.
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

def showTables ( ) :
	command = "SHOW TABLES"
	cursor.execute(command)
	tableList = cursor.fetchall()
	
	for table in tableList :
		print table[0]

#colDict is a mapping of col name to data type
def createTable ( name, dataTypes ) :
	global colFormat
	
	command = "CREATE TABLE " + name + " ("
	
	for x in range(len(colFormat)):
		command += colFormat[x] + " " + dataTypes[x] +"," 

	command = command[:-1]
	command += ")"
	executeCommand(command)
	return
		
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
def pushData ( rowDict ) :
	global activeTable
	global colFormat
	global cursor
	
	#ensure precons are met and cardinality of input data matches col set.
	initCheck ( )
	
	
	jDelim = ', '
	
	addEntry = "INSERT INTO " + activeTable
	cols = "("
	vals = "("
	
	for key in rowDict :
			cols += key + ","
			if key == "time" :
				vals += "\"" + rowDict[key] + "\","
			else :
				vals += rowDict[key] + ", "
	
	print addEntry + " " + cols[:-1] + ") VALUES " + vals[:-1] + ")"
	addEntry += " " + cols[:-1] + ") VALUES " + vals[:-1] + ")"
	
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
colFormat = ["username", "password", "tablename"]	
dataTypes = [ "VARCHAR(30)", "VARCHAR(30)", "VARCHAR(30)"]
testDict = { "time" : '2015-10-06 06:27:29', "s1" : '16', "s2" : '33', "s3" : '9', "temp" : '67' }
initConfig( )
connectDB( )
showTables()
pushData(testDict)
closeDB( )
