import requests
from calendar import Calendar, monthrange
import creds
from datetime import date, timedelta

# def date_range(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)


def is_future(date):
    '''
    @param date: datetime obj
    '''
    today = date.today()
    return date >= today

def get_current_weather(station_id, api_key):
    '''
    @param statdion_id: Private Weather Station's ID from WeatherUnderground
    @param api_key: User API key
    '''
    
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/observations/current?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&apiKey={api_key}'
    
    # fetch data
    r = requests.get(url)
    return r


def get_daily_weather(station_id, api_key, year, month, day):
    '''
    @param statdion_id: Private Weather Station's ID from WeatherUnderground
    @param api_key: User API key
    @param date: the day for which data is to be retrieved (YYYYMMDD)
    '''

    # first things first
    if is_future(date(year, month, day)) is True:
        # print("I can't predict the future!")
        return None
    
    if len(str(day)) < 2:
        day = '0' + str(day)

    if len(str(month)) < 2:
        month = '0' + str(month)
        
    # variables
    numericPrecision = 'decimal'
    format = 'json'
    units = 'm'
    url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&numericPrecision={numericPrecision}&format={format}&units={units}&date={year}{month}{day}&apiKey={api_key}'
    print(url)

    # fetch data
    r = requests.get(url)
    return r


def get_monthly_weather(station_id, api_key, year, month):
    '''
    @param statdion_id: Private Weather Station's ID from WeatherUnderground
    @param api_key: User API key
    @param year: year for which data is to be retrieved (YYYY)
    @param month: month for which data is to be retrieved (1-12)
    '''

    # created to iterate calendar
    c = Calendar()

    # list to collect responses from WU's server
    rl = []
    for date in [x for x in c.itermonthdates(year, month) if x.month == month]:
        # remove separator from datetime.date objects
        date = str(date).replace('-', '')

        # get measurements for each day of a month
        r = get_daily_weather(station_id, api_key, int(date[0:4]), int(date[4:6]), int(date[-2:]))
        if r != None:
            rl.append(r)

    if len(rl) != 0:
        return rl
    else:
        return None


def get_yearly_weather(station_id, api_key, year):
    '''
    @param statdion_id: Private Weather Station's ID from WeatherUnderground
    @param api_key: User API key
    @param year: year for which data is to be retrieved (YYYY)
    @param month: month for which data is to be retrieved (1-12)
    '''
    # list to collect sublists with responses from WU's server
    l = []
    months = range(1, 13)

    # this will create a list of lists
    for month in months:
        r = get_monthly_weather(station_id, api_key, year, month)
        if r !=  None:
            l.append(r)

    # let's flatter the list using list conprehension
    if len(l) != 0:
        rl = [item for sublist in l for item in sublist]
        return rl
    else:
        return None


def get_weather(station_id, api_key, year, month = None , day = None):
    '''
    @param statdion_id: Private Weather Station's ID from WeatherUnderground
    @param api_key: User API key
    @param year: year for which data is to be retrieved (YYYY). Optional.
    @param month: month for which data is to be retrieved (1-12). Optional.
    '''
    
    if day != None:
        r = get_daily_weather(station_id, api_key, year, month, day)
        return r
    elif day == None and month != None:
        r = get_monthly_weather(station_id, api_key, year, month)
        return r
    else:
        r = get_yearly_weather(station_id, api_key, year)
        return r


# def get_perdiod_weather(station_id, api_key, start_date, end_date):
#     '''
#     @param statdion_id: Private Weather Station's ID from WeatherUnderground
#     @param api_key: User API key
#     @param start_date: YYYYMMDD
#     @param end_date: YYYYMMDD
#     '''
#     rl = []
#     for date in date_range(start_date, end_date):
#         # remove separator from datetime.date objects
#         date = str(date).replace('-', '')

#         # get measurements for each day of a month
#         r = get_daily_weather(station_id, api_key, date)
#         if r != None:
#             rl.append(r)
    
#     if len(rl) != 0:
#         return rl
#     else:
#         return None
