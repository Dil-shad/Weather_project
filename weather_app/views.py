from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
import requests


def get_weather_data(key, lat, lon, time):
    ''' we fetching weather data by using requests '''
    try:
        # open api endpoint
        try:
            url = 'https://api.openweathermap.org/data/2.5/forecast'
            query = {
                'lat': lat,
                'lon': lon,
                'appid': key,
            }

            # parsing request with query params
            response = requests.get(url, params=query)
            response.raise_for_status()
            # fetched weather data
            weather_data = response.json()
        except Exception as e:
           print(f"Fetching weather data failed{e}")
           return HttpResponse("service unavailable now!")
           

        requested_time = datetime.strptime(time, '%H:%M')
        # using min function to find closest time , from fetched weather data based on absolute timestamp 
        closest_time = min(weather_data['list'], key=lambda x: abs(datetime.fromtimestamp(x['dt']) - requested_time))

        data = {
            'temperature':closest_time['main']['temp'],
            'weather_condition':closest_time['weather'][0]['description'], 
            'humidity':closest_time['main']['humidity']
        }

        return data
    except Exception as e:
        print(f' Error data call {e}')
        return None


def weather_forecast_lookup(request):
    """ Weather data for calicut , with temperature,humidity and weather condition , with fixed coordinates"""
    lat = 11.2588
    lon = 75.7804
    key = 'e4dc53ac469bb81befdae7bda946d3e4'

    if request.method == 'POST':
        # getting specific time from user side
        user_time = request.POST.get('time', '')
        try:
            # validating time format
            datetime.strptime(user_time, '%H:%M')
        except Exception as e:
            # handling Exception if time is not valid
            return HttpResponse("Invalid time format !")

        # calling weather data function for get the real time weather data from server side
        weather_data = get_weather_data(key, lat, lon, user_time)
        
        # if weather data not None then return
        if weather_data:
            return render(request, 'index.html',{'weather_data': weather_data})
        else:
            HttpResponse(" service unavailable now!")
            
    return render(request, 'index.html')
