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
import shutil


path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
downloadpath = '/Users/Fabian/Downloads/'
baseurl = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch?form'

# time to wait in to check whether file was downloaded
t1 = 5

# create a new session
driver = webdriver.Chrome('/Users/Fabian/Documents/DATA/Python/chromedriver')

for i in range(6, 76):

    # Info
    print('Uploading part{}.csv'.format(i))

    # Open url
    driver.get(baseurl)

    # Setup Dropdowns
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/div/div[1]/select/option[3]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/div/div[2]/select/option[2]').click()
    # driver.implicitly_wait(1)

    # Upload
    file_input = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/input[1]')
    file_input.send_keys(path + 'files/part{}.csv'.format(i))
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/input[2]').click()
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/form/input[2]').click()
    except:
        pass

    # Info
    print('file uploaded')

    # Set Timer back
    time_temp = 0

    # Wait Until Downlaoded
    FileDownloaded = False
    while FileDownloaded is False:
        # Check whether file exists, if not, wait t1
        if os.path.exists(downloadpath + 'GeocodeResults.csv') is False:
            # driver.implicitly_wait(10)
            time.sleep(t1)
            time_temp = time_temp + t1
            print('waiting for part{}.csv ... {} seconds left'.format(i, time_temp))

            if os.path.exists(path + 'downloads/GeocodeResults{}.csv'.format(i)) is True:
                FileDownloaded = True

        else:
            # If exists, wait again to make sure it's downloaded
            driver.implicitly_wait(1)
            time.sleep(1)

            # Rename and Move
            os.rename(downloadpath + 'GeocodeResults.csv', downloadpath + 'GeocodeResults{}.csv'.format(i))
            shutil.move(downloadpath + 'GeocodeResults{}.csv'.format(i), path + 'downloads/GeocodeResults{}.csv'.format(i))

            # Closing and continuing with next
            print('GeocodeResults{}.csv successfully downloaded, closing current driver and continue with next'.format(i))
            driver.implicitly_wait(1)
            driver.close()

            # Set Flag
            FileDownloaded = True


print('Everything downloaded')
