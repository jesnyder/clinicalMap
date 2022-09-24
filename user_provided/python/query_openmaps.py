from bs4 import BeautifulSoup
import datetime
import json
import math
import numpy as np
import os
import pandas as pd
import random
import re
import requests
import time
import urllib.request

from admin import print_progress
from admin import reset_df
from admin import retrieve_df
from admin import retrieve_json
from admin import retrieve_path
from admin import save_json


def query_openmaps():
    """
    create geolocated.csv
    create geolocated.json
    create locations_missing.csv
    """

    # reset the list of missing locations
    report_missing('reset')

    responses = []

    # establish locations df
    df = retrieve_df('location')

    found_locs = []
    lats = []
    lons = []

    locations = list(df['location'])
    for loc in locations:

        lat, lon, response = lookup_openmaps(loc)

        print('lat = ')
        print(lat)

        found_locs.append(str(loc))
        lats.append(lat)
        lons.append(lon)

        df_temp = pd.DataFrame()
        df_temp['location'] = found_locs
        df_temp['lat'] = lats
        df_temp['lon'] = lons
        df_temp.to_csv(retrieve_path('geolocated'))

        if lat == 0: report_missing(loc)

        responses.append(response)
        response_dict = {}
        response_dict['item_count'] = len(responses)
        response_dict['response'] = responses
        save_json(response_dict, 'geolocated_json')


def report_missing(loc):
    """
    list affiliations that don't return a location
    """

    if loc == 'reset':
        df = pd.DataFrame()
        df['location'] = []
        df.to_csv(retrieve_path('location_missing'))

    else:
        df = retrieve_df('location_missing')
        locs = list(df['location'])
        locs.append(loc)
        df = pd.DataFrame()
        df['location'] = loc
        df = reset_df(df.sort_values(by='location'))
        df.to_csv(retrieve_path('location_missing'))


def lookup_openmaps(loc):
    """
    return lat and lon
    """

    try:

        if ',' in loc:
            terms = loc.split(',')
        else:
            terms = [loc]

        for i in range(len(terms)):

            address = terms[i:]
            address = str(' '.join(address))
            address = re.sub(r'[^a-zA-z0-9\s_]+', ' ', address)
            print('address = ')
            print(address)

            specific_url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            url_response = requests.get(specific_url)

            try:
                text = url_response.text
                response = json.loads(text)
                lat = response[0]["lat"]
                lon = response[0]["lon"]
                return(lat, lon, response[0])

            except:
                continue

        return(0, 0, 0)

    except:
        return(0, 0, 0)
