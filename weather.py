import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY') # Silly me :)

def get_weather_forecast(search_word):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={search_word}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    if response.status_code != 200:
        return {}, response.status_code
    
    date = response.json()['forecast']['forecastday'][0]['date']
    dict = {}
    for i in range(0, 24):
        endpoint = response.json()['forecast']['forecastday'][0]['hour'][i]
        data = [endpoint['temp_c'], endpoint['wind_kph']]
        dict[response.json()['forecast']['forecastday'][0]['hour'][i]['time'].strip(date)] = data

    return dict, response.status_code

def get_current_state(search_word):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={search_word}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    if response.status_code != 200:
        return "", "", response.status_code
    
    time_rn = response.json()['location']['localtime']    
    temp = response.json()['current']["temp_c"]
    icon = response.json()['current']["condition"]["icon"]
    
    return time_rn, temp, icon, response.status_code

def get_cities() -> list:
    lst = []
    with open('world_cities_geoname.csv', encoding='utf-8') as csv_f:
        csv_reader = csv.reader(csv_f, delimiter=",")
        for row in csv_reader:
            lst.append(row[2]+", " + row[7])
    
    return lst
