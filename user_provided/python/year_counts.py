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
from admin import  retrieve_ref
from admin import save_json

from list_trials import list_location
from write_geojson import calculate_color
from write_geojson import find_date


def year_counts():
    """
    create year_counts_pdf.csv
    create year_counts_cdf.csv
    """

    # retrieve groups.csv
    df = retrieve_df('groups')

    years = np.arange(1994, 2024, 1)

    df_count = pd.DataFrame()
    df_count['year'] = years

    for col in df.columns:

        if col == 'url': continue

        counts = []
        enrolleds = []

        for year in years:

            count = 0
            enrolled = 0

            df_new = df[df[col] > 0]
            urls = list(df_new['url'])

            trials = retrieve_json('trials')['trials']
            for trial in trials:

                url = trial['URL']

                if url not in urls: continue

                year_found, month, day = find_date(trial)

                """
                date_found = trial['Start Date']
                date_split = date_found.split(' ')
                for item in date_split:
                    if item.isdigit() and len(item) == 4:
                        year_found = item
                        # print('year_found = ' + str(year_found))
                """

                if int(year_found) != int(year): continue

                count = count + 1
                enrolled = enrolled + int(trial['Enrollment'])

            counts.append(count)
            enrolleds.append(enrolled)

        #df_count = pd.DataFrame()
        #df_count['year'] = years
        df_count[str(col + '_count')] = counts
        df_count[str(col + '_enrolled')] = enrolleds
        df_count.to_csv(retrieve_path('year_counts_pdf'))




    cdf_counts()
    count_percent()
    enrolled_percent()

    # make js for plotting
    # retrieve trials.json
    js_count()
    js_enrolled()
    js_cdf_count()
    js_cdf_enroll()



def js_cdf_enroll():
    """

    """

    df = retrieve_df('year_counts_cdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' not in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['text'] = 'Enrolled CDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-cdf_enroll"), '
        dst_json = os.path.join(retrieve_path('cdf_js_enroll'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()



def js_cdf_count():
    """

    """

    df = retrieve_df('year_counts_cdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['text'] = 'Trial Count CDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-cdf_count"), '
        dst_json = os.path.join(retrieve_path('cdf_js_count'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()



def js_enrolled():
    """

    """

    df = retrieve_df('year_counts_pdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' not in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['test'] = 'Enrolled PDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-enroll"), '
        dst_json = os.path.join(retrieve_path('pdf_js_enrolled'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()


def js_count():
    """

    """

    df = retrieve_df('year_counts_pdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['test'] = 'PDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart"), '
        dst_json = os.path.join(retrieve_path('pdf_js'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()



def cdf_counts():
    """
    create year_counts_pdf.csv
    create year_counts_cdf.csv
    """

    # retrieve groups.csv
    df = retrieve_df('year_counts_pdf')
    df_cdf  = pd.DataFrame()

    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] <= year]

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        for col in df_year.columns:

            if col == 'year': continue

            df_temp[col] = sum(list(df_year[col]))

        df_cdf = df_cdf.append(df_temp)
        df_cdf.to_csv(retrieve_path('year_counts_cdf'))


def count_percent():
    """

    """

    df = retrieve_df('year_counts_pdf')
    df_per = pd.DataFrame()


    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] == year]
        #print(df_year)

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        allo = int(list(df_year['allo_count'])[0])
        auto = int( list(df_year['auto_count'])[0])
        both = int(list(df_year['both_count'])[0])

        sum = allo + auto + both

        if sum == 0: sum = 1

        df_temp['allo'] = [allo/sum]
        df_temp['auto'] = [auto/sum]
        df_temp['both'] = [both/sum]

        df_per = df_per.append(df_temp)
        df_per.to_csv(retrieve_path('count_percent'))


def enrolled_percent():
    """

    """

    df = retrieve_df('year_counts_pdf')
    df_per = pd.DataFrame()


    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] == year]
        #print(df_year)

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        allo = int(list(df_year['allo_enrolled'])[0])
        auto = int( list(df_year['auto_enrolled'])[0])
        both = int(list(df_year['both_enrolled'])[0])

        sum = allo + auto + both

        if sum == 0: sum = 1

        df_temp['allo'] = [allo/sum]
        df_temp['auto'] = [auto/sum]
        df_temp['both'] = [both/sum]

        df_per = df_per.append(df_temp)
        df_per.to_csv(retrieve_path('enrolled_percent'))
