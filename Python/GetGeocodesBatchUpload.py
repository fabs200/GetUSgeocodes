# -*- coding: utf-8 -*-
"""
@author: fabian.nemeczek@ecb.europa.eu
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os # process directories
import glob # processing directories
import shutil # handling file moving, renaming
import time
import pandas as pd
import csv

path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
baseurl = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch?form'

# time to wait in sec. when page (re)loads
t1 = 60

# create a new session
driver = webdriver.Chrome('/Users/Fabian/Documents/DATA/Python/chromedriver')
driver.implicitly_wait(10)

for i in range(1, 76):
    driver.get(baseurl)

    # Setup Dropdowns
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/div/div[1]/select/option[3]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/div/div[2]/select/option[2]').click()
    driver.implicitly_wait(10)

    # Upload
    file_input = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/input[1]')
    file_input.send_keys(path + 'files/part{}.csv'.format(i))
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/input[2]').click()

    # Wait Until Downlaoded
    time.sleep(t1)

