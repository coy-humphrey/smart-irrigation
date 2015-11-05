from flask import Flask, request, jsonify, redirect, url_for
from flaskext.mysql import MySQL
import os
import ConfigParser
import MySQLdb
import json
import collections
import math
from time import time
from datetime import datetime, timedelta

mysql = MySQL()
application = Flask(__name__)
config = ConfigParser.ConfigParser()


configdir = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(configdir, "config", "configAPI.ini")
config.read(configpath)

# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'password': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'database': config.get('MySQL', 'database'),
  'raise_on_warnings': True,
}

application.config['MYSQL_DATABASE_USER'] = sql_config["user"]
application.config['MYSQL_DATABASE_PASSWORD'] = sql_config["password"]
application.config['MYSQL_DATABASE_DB'] = sql_config["database"]
application.config['MYSQL_DATABASE_HOST'] = sql_config["host"]

#create a function here which will automatically return a return a cursor with executed query
#def select_query(args:)


@application.route('/')
def api_root():
  return redirect(url_for('api_mygarden'))

@application.route('/mygarden')
def api_mygarden():
  return "MyGarden Home Page"

@application.route('/mygarden/watering_graph')
def api_watergraph():
  return "Watering Graph Here"

#calculate average temperature by weeks
@application.route('/mygarden/temperature_graph', methods=['GET'])
def api_tempgraph():

  conn = MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
    passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])
  cursor = conn.cursor()

  query = ("SELECT time, temp FROM entry")
  cursor.execute(query)

  temp_rows = cursor.fetchall()
  objects_list = []
  avg_temp = 0
  day_count = 0
  prev_week = temp_rows[0][0].isocalendar()[1]

  for row in temp_rows:
    d = collections.OrderedDict()
    month = row[0].month
    full_date = row[0]
    year, week, dow = full_date.isocalendar()
    temp = row[1]
    if week == prev_week:
      avg_temp += temp
    else:
      d['avg_temp'] = math.ceil(avg_temp/day_count)
      objects_list.append({full_date.strftime("%B") + ", " + str(year) + ' Week: ' + str(prev_week): d})
      day_count = 0
      avg_temp = temp
    prev_week = week
    day_count += 1
  conn.close()

  return jsonify({'Avg Week Temperatures': objects_list})

  #date_obj = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
  #week = date_obj.isocalendar()[1]

#json every sensor temperature reading with dates
@application.route('/mygarden/temperature_graph/individual', methods=['GET'])
def api_tempgraph_individual():

  conn = mysql.connect()
  cursor = conn.cursor()

  query = ("SELECT time, temp FROM entry")
  cursor.execute(query)

  temp_rows = cursor.fetchall()
  objects_list = []
  
  for row in temp_rows:
    d = collections.OrderedDict()
    month = row[0].month
    full_date = row[0]
    temp = row[1]
    year, week, dow = full_date.isocalendar()
    d['time'] = full_date
    d['temp'] = temp
    d['week'] = week
    d['year'] = year
    objects_list.append(d)
  conn.close()
  return jsonify({'All temperature readings': objects_list})

#simply returns all sensor readings in JSON format
@application.route('/sensor_table', methods=['GET'])
def api_sensors():

  conn = mysql.connect()
  cursor = conn.cursor()

  query = ("SELECT time, s1, s2, s3, temp FROM entry")
  cursor.execute(query)

  sensor_rows = cursor.fetchall()

  objects_list = []
  for row in sensor_rows:
    d = collections.OrderedDict()
    d['time'] = row[0]
    d['s1'] = row[1]
    d['s2'] = row[2]
    d['s3'] = row[3]
    d['temp'] = row[4]
    objects_list.append(d)
  conn.close()

  return jsonify({'sensors': objects_list})

if __name__ == '__main__':

  mysql.init_app(application)
  application.run(debug=True)
    
