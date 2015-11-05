from flask import Flask, request, jsonify, redirect, url_for
from flaskext.mysql import MySQL
import os
import ConfigParser
import MySQLdb
import json
import collections
import math
from time import time
from datetime import datetime

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


@application.route('/')
def api_root():
  return redirect(url_for('api_mygarden'))

@application.route('/mygarden')
def api_mygarden():
  return "MyGarden Home Page"

@application.route('/mygarden/watering_graph')
def api_watergraph():
  return "Watering Graph Here"

#calculate average temperature by days, weeks, months
@application.route('/mygarden/temperature_graph', methods=['GET'])
def api_tempgraph():

  conn = MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
  passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])
  cursor = conn.cursor()

  query = ("SELECT time, temp FROM entry")
  cursor.execute(query)

  temp_rows = cursor.fetchall()
  json_list = []
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
      json_list.append({full_date.strftime("%B") + ", " + str(year) + ' Week: ' + str(prev_week): d})
      day_count = 0
      avg_temp = temp
    prev_week = week
    day_count += 1
  conn.close()

  return jsonify({'Avg Week Temperatures': json_list})

@application.route('/mygarden/temperature_graph/all', methods=['GET'])
def api_tempgraph_individual():

  conn = MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
  passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])
  cursor = conn.cursor()

  query = ("SELECT time, temp FROM entry")
  cursor.execute(query)

  temp_rows = cursor.fetchall()
  json_list = []
  
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
    json_list.append(d)
  conn.close()
  return jsonify({'All temperature readings': json_list})

def parse_date(string):
  return int(string[4:8]), int(string[0:2]), int(string[2:4]) 

#<date_range> must be in the format xxyyzzzz_xxyyzzzz. Ex: 01251967_03252015 = 01/25/1967-03/25/2015
@application.route('/mygarden/temperature_graph/date/<date_range>', methods=['GET'])
def range(date_range):

  date_start, date_end = date_range.split('_')

  year, month, day = parse_date(date_start)
  date_start = datetime(year, month, day)

  year, month, day = parse_date(date_end)
  date_end = datetime(year, month, day)
  
  conn = MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
  passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])
  cursor = conn.cursor()
  query = ("SELECT time, temp FROM entry WHERE time BETWEEN '%s' and '%s'") % (date_start, date_end)
  cursor.execute(query)
  temp_rows = cursor.fetchall()

  json_list = []
  for row in temp_rows:
    d = collections.OrderedDict()
    d['time'] = row[0]
    d['temp'] = row[1]
    json_list.append(d)
  conn.close()

  return jsonify({'sensors': json_list})


@application.route('/sensor_table', methods=['GET'])
def api_sensors():

  conn = MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
  passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])
  cursor = conn.cursor()

  query = ("SELECT time, s1, s2, s3, temp FROM entry")
  cursor.execute(query)

  sensor_rows = cursor.fetchall()

  json_list = []
  for row in sensor_rows:
    d = collections.OrderedDict()
    d['time'] = row[0]
    d['s1'] = row[1]
    d['s2'] = row[2]
    d['s3'] = row[3]
    d['temp'] = row[4]
    json_list.append(d)
  conn.close()

  return jsonify({'sensors': json_list})

if __name__ == '__main__':

  mysql.init_app(application)
  application.run(debug=True)
  
