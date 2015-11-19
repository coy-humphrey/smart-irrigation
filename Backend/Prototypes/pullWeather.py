import requests, os
import json
import ConfigParser

def get_api_key():
	config = ConfigParser.ConfigParser()
	parentdir= os.path.dirname(os.getcwd())
	configdir = os.path.dirname(os.getcwd())
	config.read(os.path.join(configdir, "config", "configAPI.ini"))
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
				'weather' : station["current_observation"]["weather"], 
				'precipitation_metric' : station["current_observation"]["precip_today_metric"],
				'uv' : station["current_observation"]['UV'],
				'wind_mph' : station["current_observation"]["wind_mph"],
				'pressure_in' : station["current_observation"]["pressure_in"]
			}
	print(results)
	return results
	
	


get_forecast()