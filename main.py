import requests
from datetime import datetime
from calendar import Calendar, monthrange

def get_current_weather(station_id, api_key):
    
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/observations/current?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&apiKey={api_key}'
    
    # execute
    r = requests.get(url)
    return r


def get_daily_weather(date, station_id, api_key):
    
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&date={date}&apiKey={api_key}'
    
    # execute
    r = requests.get(url)
    return r


def get_monthly_weather(year, month, station_id, api_key):
    c = Calendar()
    history = []
    for date in [x for x in c.itermonthdates(year, month) if x.month == month]:
        # remove separator from datetime.date objects
        date = str(date).replace('-', '')

        # get measurements for each day of a month
        history.append(get_daily_weather(date, station_id, api_key))
    return history
