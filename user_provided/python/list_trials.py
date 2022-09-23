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

from admin import reset_df
from admin import retrieve_df
from admin import retrieve_path
from admin import retrieve_json
from admin import save_json


def list_trials():
    """
    Objective
    Map clinical trials
    """

    time_begin = datetime.datetime.today()
    print('begin list_trials ' + str(time_begin))

    trials = []

    src = retrieve_path('clinical_src')
    for file in os.listdir(src):

        df = retrieve_df(os.path.join(src, file))

        items = list(df['NCT Number'])

        for item in items:

            i = items.index(item)

            trial = {}

            for col in df.columns:

                if col == 'Rank': continue

                value = df.at[i, col]
                trial[col] = str(value)

            if trial in trials: continue
            trials.append(trial)

        trials_dict = {}
        trials_dict['item_count'] = len(trials)
        trials_dict['trials'] = trials
        save_json(trials_dict, 'trials')

    list_locations()

    time_end = datetime.datetime.today()
    print('completed list_trials ' + str(time_end))


def list_locations():
    """
    create list of locations
    locations.csv
    """

    locations = []

    trials = retrieve_json('trials')['trials']

    for trial in trials:

        location = trial['Locations']

        location_list = list_location(location)

        for item in location_list:

            if item in locations: continue
            locations.append(item)

        df = pd.DataFrame()
        df['location'] = locations
        df = reset_df(df.sort_values(by='location'))
        df.to_csv(retrieve_path('location'))


def list_location(location):
    """
    return a list of locations
    """

    location_list = []

    if '|' in location:

        loc = location.split('|')

        for item in loc:
            if item in location_list: continue
            location_list.append(item)

    else:
        location_list = [location]

    return(location_list)
