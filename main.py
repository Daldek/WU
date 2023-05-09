import requests
from calendar import Calendar, monthrange
import creds

def get_current_weather(station_id, api_key):
    
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/observations/current?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&apiKey={api_key}'
    
    # execute
    r = requests.get(url)
    return r


def get_daily_weather(station_id, api_key, date):
    
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&date={date}&apiKey={api_key}'
    
    # execute
    r = requests.get(url)
    return r


def get_monthly_weather(station_id, api_key, year, month):
    c = Calendar()
    r = []
    for date in [x for x in c.itermonthdates(year, month) if x.month == month]:
        # remove separator from datetime.date objects
        date = str(date).replace('-', '')

        # get measurements for each day of a month
        r.append(get_daily_weather(station_id, api_key, date))
    return r


def get_yearly_weather(station_id, api_key, year):
    l = []
    months = range(1, 13)

    # this will create a list of lists
    for month in months:
        l.append(get_monthly_weather(station_id, api_key, year, month))

    # let's flatter the list using list conprehension
    r = [item for sublist in l for item in sublist]
    return r


def get_perdiod_weather(station_id, api_key, start_date, end_date):
    pass
