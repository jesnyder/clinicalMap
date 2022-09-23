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

from list_trials import list_location


def assign_groups():
    """
    create geojson for each group
    """

    time_begin = datetime.datetime.today()
    print('begin assign_groups ' + str(time_begin))

    urls, allos, autos, boths, undeclareds = [], [], [], [], []

    trials = retrieve_json('trials')['trials']
    for trial in trials:

        url = str(trial['URL'])
        if url in urls: continue

        print(round(trials.index(trial) / len(trials) * 100, 3))

        int = trial['Interventions']

        allo = 0
        allo_terms = list(retrieve_df('allo_terms')['term'])
        if term_found(int, allo_terms) == True: allo = 1

        auto = 0
        auto_terms = list(retrieve_df('auto_terms')['term'])
        if term_found(int, auto_terms) == True: auto = 1

        both = 0
        if allo == 1 and auto == 1: allo, auto, both = 0, 0, 1

        undeclared = 0
        if allo + auto + both == 0: undeclared = 1

        #print(allo + auto + both + undeclared)
        assert allo + auto + both + undeclared == 1

        urls.append(url)
        allos.append(allo)
        autos.append(auto)
        boths.append(both)
        undeclareds.append(undeclared)

    # save dataframe with group assignments
    df = pd.DataFrame()
    df['url'] = urls
    df['all'] = [1]*len(urls)
    df['allo'] = allos
    df['auto'] = autos
    df['both'] = boths
    df['undeclared'] = undeclareds
    df = reset_df(df.sort_values(by='url'))
    df.to_csv(retrieve_path('groups'))

    time_end = datetime.datetime.today()
    print('completed assign_groups ' + str(time_end))


def term_found(ref, terms):
    """
    return True if term found ref text
    """

    ref = re.sub(r'[^a-zA-z0-9\s_]+', ' ', ref)
    ref = str(ref.lower())

    for term in terms:

        term = re.sub(r'[^a-zA-z0-9\s_]+', ' ', term)
        term = str(term.lower())

        if term not in ref: continue
        return(True)

    return(False)
