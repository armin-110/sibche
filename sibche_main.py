print('بسمه الله الرحمن الرحیم')
print('salam bar mohammadreza dehghan amiri')
import datetime
from sqlalchemy import create_engine
import schedule
import itertools
import time
from iteration_utilities import unique_everseen
from collections import OrderedDict
import requests
from copy import deepcopy
import copy
import json
import re
from bs2json import bs2json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as b
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from rich import print
from curses import COLOR_BLACK

import sibche_get_link
import sibche_meta

def get_total_links(page_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = sibche_get_link.Getmorelinks(driver, page_link)
    gf.get_link()
    driver.close()
    return (sibche_get_link.total_link[0])


def get_metadata(content_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = sibche_meta.Getmeta(driver, content_link)
    gf.get_meta()
    driver.close()
    return (sibche_meta.meta_list)
###################################################################################
date_a=datetime.datetime.now()
engine = create_engine('postgresql://postgres:12344321@10.32.141.17/sibche',pool_size=20, max_overflow=100,)
con=engine.connect()

# get_total_links('https://sibche.com/pages/app') 
# get_total_links('https://sibche.com/pages/game')
# page_link=get_total_links('https://sibche.com/pages/game')
# print(page_link)
# print(get_metadata('https://sibche.com/applications/promax-gps'))
# print(get_metadata('https://sibche.com/applications/%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7%D9%86%DA%A9-%D9%85%D9%84%D8%AA'))
# for i in range(len(page_link)):
#     print(get_metadata(page_link))

#step1: program categori crawling
# page_link=get_total_links('https://sibche.com/pages/app') 
# error_link=[]
# for i in range(len(page_link)):
#     link_meta=get_metadata(page_link[i])
#     if link_meta[0]['content_name']=='':
#         link_meta=get_metadata(page_link[i])
#     if link_meta[0]['content_name']=='':
#        error_link.append(page_link[i]) 
#     date_i=datetime.datetime.now()
#     link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
#     link_meta[0]['cat']='program'
#     data_frame =pd.DataFrame(link_meta[0],index=[0])
#     data_frame.to_sql('sibche_meta'+str(date_a.date()).replace('-','')+str(date_a.time()).split(':')[0],con,if_exists='append', index=False)
#     print(link_meta)
# if len(error_link)>0:
#     for i in range(len(error_link)):
#         link_meta=get_metadata(error_link[i])
#         if link_meta[0]['content_name']=='':
#             link_meta=get_metadata(error_link[i])
#         # if link_meta[0]['content_name']=='':
#         # error_link.append(page_link[i]) 
#         date_i=datetime.datetime.now()
#         link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
#         link_meta[0]['cat']='program'
#         data_frame =pd.DataFrame(link_meta[0],index=[0])
#         data_frame.to_sql('sibche_meta'+str(date_a.date()).replace('-','')+str(date_a.time()).split(':')[0],con,if_exists='append', index=False)
#         print(link_meta)


# #step2:game categori crawling
page_link1=get_total_links('https://sibche.com/pages/game')
error_link=[]
for i in range(len(page_link1)):
    link_meta=get_metadata(page_link1[i])
    if link_meta[0]['content_name']=='':
        link_meta=get_metadata(page_link1[i])
    if link_meta[0]['content_name']=='':
       error_link.append(page_link1[i]) 
    date_i=datetime.datetime.now()
    link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
    link_meta[0]['cat']='game'
    data_frame =pd.DataFrame(link_meta[0],index=[0])
    data_frame.to_sql('sibche_meta',con,if_exists='append', index=False)
    print(link_meta)
if len(error_link)>0:
    for i in range(len(error_link)):
        link_meta=get_metadata(error_link[i])
        if link_meta[0]['content_name']=='':
            link_meta=get_metadata(error_link[i])
        # if link_meta[0]['content_name']=='':
        # error_link.append(page_link[i]) 
        date_i=datetime.datetime.now()
        link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
        link_meta[0]['cat']='game'
        data_frame =pd.DataFrame(link_meta[0],index=[0])
        data_frame.to_sql('sibche_meta',con,if_exists='append', index=False)
        print(link_meta)



#step3: 
import psycopg2
import pandas.io.sql as psql
connection = psycopg2.connect(user="postgres",
                                password="12344321",
                                host="10.32.141.17",
                                port="5432",
                                database="sibche")
cursor = connection.cursor()

df0= psql.read_sql("SELECT * FROM public.sibche_meta", connection)
print(len(df0))
cursor.execute("DELETE FROM public.sibche_meta")
connection.commit()
if connection:
    cursor.close()
    connection.close()
df0.drop_duplicates(subset =["content_link"],
                    keep = 'last', inplace = True)
print(len(df0))
engine = create_engine('postgresql://postgres:12344321@10.32.141.17/sibche',pool_size=20, max_overflow=100,)
con=engine.connect()
df0.to_sql('sibche_meta'+str(date_a.date()).replace('-','')+str(date_a.time()).split(':')[0],con,if_exists='append', index=False)
con.close()