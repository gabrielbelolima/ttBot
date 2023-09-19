#!/usr/bin/env python
# coding: utf-8

# # Funções

# ## Importing libs

import os
import requests
import tweepy
from datetime import datetime as dt

# ## Auth

tt = tweepy.Client(
    #Consumer Keys
    consumer_key= os.environ['CONSUMER_KEY'],
    consumer_secret= os.environ['CONSUMER_SECRET'],
    # Access Token and Secret
    access_token= os.environ['ACCESS_TOKEN'],
    access_token_secret= os.environ['ACCESS_TOKEN_SECRET'])

# ## Defining Functions

now = dt.now()

#- get_date()
def get_date(year=None, month=None, day=None, now=now, as_str=True):
    """Returns string with the actual month and year, or especified date.
  Used in request url.

  in: get_month()
  out: <ACTUAL_YEAR>/<ACTUAL_MONTH>/

  in: get_month(year = 2010, month = 03)
  out: 2010/marco"""

    if year == None:
        year_n = now.year
    else:
        year_n = year

    if month == None:
        month_n = now.month
    else:
        month_n = month

    day_n = now.day

    dt_month = dict(
        zip(range(1, 13), [
            'janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
            'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
        ]))

    if as_str == True:
        str_date = '{}/{}'.format(year_n, dt_month[month_n])
    else:
        str_date = [year_n, month_n, day_n]

    return str_date


#- create_tree()
def create_tree(year=None, month=None):

    # sets month and year for request ()
    str_date = get_date(year, month)

    # Scrap's Resquest
    url_r = 'https://www.datascomemorativas.me/{}'.format(str_date)
    with requests.get(url_r) as r:
        #print('DEBUG - status code: ',r.status_code)
        r.encoding = 'UTF-8'
        text = r.text  # string
        #content = r.content # bytes

    # generates html tree from html string
    from lxml import html
    tree = html.fromstring(text)
    return tree


#- create_grid()
def create_grid(year=None, month=None, full_grid=False):

    # today's date
    today = get_date(as_str=False)

    if year == None:
        year = today[0]

    month_n = today[1] if month == None else month

    html_tree = create_tree(year, month)

    x = list(range(1, 7))  # week of the month (1 = first week)
    y = list(range(1, 8))  # day of the week (1 = sunday, 7 = saturday)
    z = list(range(
        1, 10))  # 9 rows per day (row1: icecream day, row2: youscream day)

    # Creates Grid
    from itertools import product
    l = list(product(x, y, z))  # Vectorial product of lists

    # Sets up grid loop
    content = None
    date_list = []

    # defines year
    year_xpath = '/html/body/section/div/header/div[1]/span[2]'
    year = int(html_tree.xpath(year_xpath)[0].text_content())

    # defines month
    month_xpath = '/html/body/section/div/header/div[1]/span[1]'
    month = html_tree.xpath(month_xpath)[0].text_content()

    # Searchs html-tree using the grid
    for x in range(len(l)):
        a, b, c = l[x][0], l[x][1], l[x][2]
        xpath_ref = [a, b, c]
        # If a month starts on monday (week day 2), then the Sunday (day =1) returns Day = None
        try:
            #Defines day
            day_xpath = '/html/body/section/div/div/table/tbody/tr[{0}]/td[{1}]/div[1]/span[1]'.format(
                a, b)
            day = html_tree.xpath(day_xpath)[0].text_content()
        except:
            day = 0

        try:
            content_xpath = '/html/body/section/div/div/table/tbody/tr[{0}]/td[{1}]/ul/li[{2}]/span'.format(
                a, b, c)
            content = html_tree.xpath(content_xpath)[0].text_content()
        except:
            content = None

        date_list.append([year, month_n, int(day), content, str(xpath_ref)])

        if full_grid == False:
            date_list = [x for x in date_list if x[3] != None
                         ]  # Filters grid: content != None. See *** bellow

    return date_list


#- todays_tt()
def todays_tt():
    today = get_date(as_str=False)
    date_list = create_grid()
    tt_list = [x for x in date_list if x[:3] == today]

    return tt_list


#- format_post()
def format_post():
    ttt = todays_tt()
    ttt_aux = list(set([x[3] for x in ttt]))
    txt = str([x for x in ttt_aux]).strip('[]').replace("'", "")

    if len(ttt_aux) > 1:
        txt = txt.replace(',{}'.format(txt.split(',')[-1]),
                          ' e{}'.format(txt.split(',')[-1]))

    if txt == '':
        return 'Hoje não temos datas comemorativas! 😥'
    else:
        return 'Hoje é {}'.format(txt)


#- post_date()
def post_date():
    text = format_post()
    r = tt.create_tweet(text=text)
    print(r)
    return
