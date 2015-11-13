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
print configpath
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

def get_conn():
  return MySQLdb.connect(host=application.config['MYSQL_DATABASE_HOST'], user=application.config['MYSQL_DATABASE_USER'],
  passwd=application.config['MYSQL_DATABASE_PASSWORD'], db=application.config['MYSQL_DATABASE_DB'])

@application.route('/')
def api_root():
  return redirect(url_for('api_mygarden'))

@application.route('/mygarden')
def api_mygarden():
  return "MyGarden Home Page"

@application.route('/mygarden/watering_graph')
def api_watergraph():
  return "Watering Graph Here"

@application.route('/mygarden/check_water', methods=['GET'])
def api_checkwater():

  conn = get_conn()
  cursor = conn.cursor()

  query = ("SELECT time, s1, s2, s3 FROM entry ORDER BY time DESC LIMIT 1")
  cursor.execute(query)
  row = cursor.fetchone()


  d = collections.OrderedDict()
  d['time'] = row[0]
  d['hour_diff'] = int(math.ceil((abs(datetime.now() - row[0])).total_seconds() / 3600))
  d['s1_watering'] = row[1] < 60 and d['hour_diff'] >= 12
  d['s2_watering'] = row[2] < 60 and d['hour_diff'] >= 12
  d['s3_watering'] = row[3] < 60 and d['hour_diff'] >= 12
  conn.close()
  return jsonify({'watering-check': d})

def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(math.ceil(adjusted_dom/7.0))

#calculate average temperature by days, weeks, months
@application.route('/mygarden/temperature_graph', methods=['GET'])
def api_tempgraph():

  conn = get_conn()
  cursor = conn.cursor()

  query = ("SELECT time, temp FROM entry")
  cursor.execute(query)

  temp_rows = cursor.fetchall()
  json_list = []
  temps = []
  prev_week = temp_rows[0][0].isocalendar()[1]

  for row in temp_rows:
    d = collections.OrderedDict()
    month = row[0].month
    full_date = row[0]
    year, week, dow = full_date.isocalendar()
    temp = row[1]
    if week == prev_week:
      temps.append(temp)
    else:
      d['max_temp'] = max(temps)
      d['avg_temp'] = int(math.ceil(reduce(lambda x, y: x + y, temps) / len(temps)))
      d['min_temp'] = min(temps)
      json_list.append({full_date.strftime("%B") + "_" + str(year) + ' Week: ' + str(prev_week): d})
      temps = [temp]
    prev_week = week
  conn.close()

  return jsonify({'week_temperatures': json_list})

@application.route('/mygarden/temperature_graph/all', methods=['GET'])
def api_tempgraph_individual():

  conn = get_conn()
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
  
  conn = get_conn()
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

  conn = get_conn()
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
  application.config["JSON_SORT_KEYS"] = False
  application.run(debug=True)
    
