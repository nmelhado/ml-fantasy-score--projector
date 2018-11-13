import datetime
import json
import requests
import os
from bs4 import BeautifulSoup

from get_specific_data import get_specific_data
from get_dst_data import get_dst_data
from get_k_data import get_k_data

global week
week = 9
global year
year = 2018
global end_year
end_year = 2018
global end_week
end_week = 9

positions = ('QB', 'WR', 'RB', 'TE')

path = '/var/www/llfantasy.com/public_html/'


def get_all_data():
    '''Loops through all weeks that data has not already been gathered
    for.'''
    global year
    global end_year
    global week
    global end_week
    reevaluate = False
    while year <= int(end_year):
        week_limit = end_week if year == end_year else 16
        while week <= week_limit:
            for position in positions:
                get_specific_data(position, year, week)
            get_dst_data(year, week)
            get_k_data(year, week)
            week += 1
            reevaluate = True
        week = 1
        year += 1
    return reevaluate


def set_limits(year, week):
    '''Sets starting week and year.'''
    global path
    filename = os.path.join(path, 'year_and_weeks.json')
    with open(filename, 'w') as info_object:
        info = {'year': year, 'week': week}
        json.dump(info, info_object)


def get_limits():
    '''Gets starting week and year, as well as end week and end year.'''
    global path
    filename = os.path.join(path, 'year_and_weeks.json')
    with open(filename) as info_object:
        info = json.load(info_object)
        print(info)
        global year
        year = info['year']
        global week
        week = info['week'] + 1
    month = datetime.datetime.now().month
    global end_year
    global end_week
    if month > 8:
        end_year = datetime.datetime.now().year
    else:
        end_year = datetime.datetime.now().year - 1
    url = 'http://www.nfl.com/schedules/' + str(end_year)
    req = requests.get(url)
    week_data = BeautifulSoup(req.text, "html.parser")
    week_full = week_data.find('h2').text
    end_week = int(week_full.split(' ')[2])
    end_week = 16 if end_week > 17 else end_week-1
    set_limits(end_year, end_week)
    return end_week + 1 if end_week > 15 else 16
