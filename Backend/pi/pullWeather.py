import requests, os
import json
import datetime
import ConfigParser
import MySQLdb

config = ConfigParser.ConfigParser()
configdir = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(os.path.dirname(configdir), "config", "configWeather.ini")
config.read(configpath)

# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'passwd': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'db': config.get('MySQL', 'database'),
}

def get_api_key():
	key = config.get('weather', 'key')
	return key

def get_closest_pws(key):
	request_url = ("http://api.wunderground.com/api/" + key +
		"/geolookup/q/autoip.json")

	json_obj = requests.get(request_url).json()
	local_stations = json_obj['location']['nearby_weather_stations']
	pws_stations = local_stations["pws"]["station"]
	station_id = pws_stations[0]["id"]
	return station_id


def get_forecast():
	key = get_api_key()
	station_id = get_closest_pws(key)
	request_url = ("http://api.wunderground.com/api/" + key +
		"/conditions/q/pws:" + station_id + ".json")
	station = requests.get(request_url).json()

	results = {
	'precipitation' : float(station["current_observation"]["precip_today_in"]),
	'solarrad' : station["current_observation"]['solarradiation'],
	'wind_speed' : float(station["current_observation"]["wind_mph"]),
	'winddegrees' : int(station["current_observation"]["wind_degrees"]),
	'humidity': int(station["current_observation"]["relative_humidity"][:-1]),
	'dewpoint_f' : int(station["current_observation"]["dewpoint_f"]),
	'pressure' : int(station["current_observation"]["pressure_mb"]),
	'time' : datetime.datetime.today().strftime('"%Y-%m-%d %H:%M:%S"')
	}

	if results['solarrad'] == '--':
		results['solarrad'] = 0
	else:
		results['solarrad'] = int(results['solarrad'])

	return results
	
def push_forecast():
	results = get_forecast()
	add_entry = ("INSERT INTO weather "
                 "(winddegrees, solarrad, precipitation, humidity, dewpoint_f, pressure, wind_speed, time) "
                 "VALUES (%(winddegrees)s, %(solarrad)s, %(precipitation)s, %(humidity)s, %(dewpoint_f)s, %(pressure)s, %(wind_speed)s, %(time)s)") % results

	conn = MySQLdb.connect(**sql_config)
	cursor = conn.cursor()
    # Perform query and fetch results
	cursor.execute(add_entry)
	conn.commit()
	cursor.close()
	conn.close()

push_forecast()
