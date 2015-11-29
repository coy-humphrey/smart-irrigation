import requests, os
import json
import ConfigParser

def get_api_key():
	config = ConfigParser.ConfigParser()
	configdir = os.path.dirname(os.getcwd())
	print(configdir)
        config.read(os.path.join(configdir, "config", "configWeather.ini"))
	print
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
				'precipitation_inches' : station["current_observation"]["precip_today_in"],
				'solar_radiation' : station["current_observation"]['solarradiation'],
				'wind_mph' : station["current_observation"]["wind_mph"],
                                'wind_degrees' : station["current_observation"]["wind_degrees"],
				'relative_humidity': station["current_observation"]["relative_humidity"],
                                'dewpoint_f' : station["current_observation"]["dewpoint_f"],
                                'pressure_mb' : station["current_observation"]["pressure_mb"]
			}
	print(results)
	return results
	
	


get_forecast()
