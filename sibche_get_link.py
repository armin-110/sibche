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
total_link=[]

class Getmorelinks():
    def __init__ (self,driver,page_link):
        self.driver=driver
        self.page_link=page_link
    def get_link(self):
        
        total_link.clear()

        try:
            try:
                self.driver.get(self.page_link)
                self.driver.refresh()
            except:
                try:
                    time.sleep(3)
                    self.driver.get(self.page_link)
                    self.driver.refresh()
                except:
                    time.sleep(3)
                    self.driver.get(self.page_link)
                    self.driver.refresh()

            converter = bs2json()
            # self.driver.get(self.page_link)

            SCROLL_PAUSE_TIME = 5
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            start1=time.time()
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_time=time.time()-start1
                print(scroll_time)


            try:
                fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div')))
            except:
                
                try:
                    fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div')))
                except:
                    print('page not loaded')
            html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
            html_soup=b(html,'html.parser')
            converter = bs2json()  

            # print(html_soup.find_all('a', href=True))
 
            link_list=[]
            for a in html_soup.find_all('a', href=True):
                if 'http' not in a['href']:
                    link_list.append('https://sibche.com'+a['href'])

            link_list_uniqe= list(dict.fromkeys(link_list))
            # print(len(link_list_uniqe))
            total_link.append(link_list_uniqe)
        except:
            print('link not founded') 
            total_link.append([])   