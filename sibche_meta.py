from curses import COLOR_BLACK
from rich import print
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import pandas as pd
import numpy as np
from bs2json import bs2json
import re
import json
import copy
from copy import deepcopy
import requests
from collections import OrderedDict
from iteration_utilities import unique_everseen
import time
import itertools
import schedule
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
import datetime
# import scrapy
meta_list=[]
class Getmeta():
    def __init__ (self,driver,content_link):
        self.driver=driver
        self.content_link=content_link
    def get_meta(self):
        meta_list.clear()
   
        try:
            try:
                self.driver.get(self.content_link)
                self.driver.refresh()
            except:
                try:
                    time.sleep(3)
                    self.driver.get(self.content_link)
                    self.driver.refresh()
                except:
                    time.sleep(3)
                    self.driver.get(self.content_link)
                    self.driver.refresh()

            converter = bs2json()
            # self.driver.get(self.page_link)

            try:
                fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]')))
            except:
                try:

                    fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]')))
                except:
                    pass

            meta_dic = {'cat':'','categori_name':'','content_name': '','content_link':self.content_link,'rate':'0','ratings':'0','Size':'','Installs':'0','Current Version':'','creator':'','age range':'','crawling_date':''}
            html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
            html_soup=b(html,'html.parser')
            converter = bs2json()
        
            class_find=html_soup.findAll('h1')
            json_class_find = converter.convertAll(class_find)
            print(json_class_find)#title
            meta_dic['content_name']=json_class_find[0]['text']
            ######
            class_find=html_soup.findAll('div',{'class':'InfoSection__DesktopWrapper-sc-1qk5bhk-2 gMgyvb'})
            json_class_find = converter.convertAll(class_find)
            # print(json_class_find[0]['div'][0]['div'][0]['text'])
            pattern = '[+,<>ا-ی]'
            for i in range(len(json_class_find[0]['div'])):
                # print(json_class_find[0]['div'][i]['div'][0]['text'])

                if json_class_find[0]['div'][i]['div'][0]['text']=='سازنده':
                    print(json_class_find[0]['div'][i]['div'][1]['a']['text'])
                    meta_dic['creator']=json_class_find[0]['div'][0]['div'][1]['a']['text']
            ########   
                if json_class_find[0]['div'][i]['div'][0]['text']=='تعداد نصب':
                    print(int(re.sub(pattern,'', json_class_find[0]['div'][i]['div'][1]['text'])))
                    # print(int(json_class_find[0]['div'][i]['div'][1]['text'].replace("+","")))
                    meta_dic['Installs']=int(re.sub(pattern,'', json_class_find[0]['div'][i]['div'][1]['text']))
            ########
                if json_class_find[0]['div'][i]['div'][0]['text']=='حجم برنامه':
                    meta_dic['Size']=json_class_find[0]['div'][i]['div'][1]['text']
                    print(json_class_find[0]['div'][i]['div'][1]['text'])
            ########
                if json_class_find[0]['div'][i]['div'][0]['text']=='نسخه فعال':
                    meta_dic['Current Version']=json_class_find[0]['div'][i]['div'][1]['span']['text']
                    print(json_class_find[0]['div'][i]['div'][1]['span']['text'])       
            ########
                if json_class_find[0]['div'][i]['div'][0]['text']=='محدودیت سنی':
                    meta_dic['age range']=json_class_find[0]['div'][i]['div'][1]['text']
                    print(json_class_find[0]['div'][i]['div'][1]['text'])   
            # print(meta_dic)
            #########################
            class_find=html_soup.findAll('div',{'class':'RateableRate__RateCount-sc-1vsa7me-1 MIdRq'})
            json_class_find = converter.convertAll(class_find)
            print(json_class_find[0]['text'])#ratingls
            meta_dic['ratings']=int(re.sub(pattern,'', json_class_find[0]['text']))

            class_find=html_soup.findAll('div',{'class':'sc-htpNat kqdWPU'})
            json_class_find = converter.convertAll(class_find)
            print(len(json_class_find))
            print(json_class_find[0])
            if json_class_find[0] !=None:
                print(json_class_find[0]['text'])#rate
                meta_dic['rate']=int(json_class_find[0]['text'])
            
            meta_list.append(meta_dic)
        except:
            meta_list.append(meta_dic)

        ######################################################
        