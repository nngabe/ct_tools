# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:07:39 2020

@author: rhysl, searri
"""


##Script to automate collecting historical posts at different intervals from CrowdTangle

from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import date, time, datetime
import pandas as pd
import traceback, logging, configparser

from ct_utils import get_driver, fb_login

'''
Creates a log file of program and enables errorFile
'''
today = date.today().strftime('%Y%m%d')
Log_File = 'HistPosts_ProgramLog_'+ str(today) +'.txt' 

logging.basicConfig(filename= Log_File, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of program')


'''
Reading Configs to store login credentials
'''
config = configparser.ConfigParser()
config.read("config.ini")

phone = config['CrowdTangle']['phone']
password = config['CrowdTangle']['password']

'''
launching the browser and logging in
'''

browser = get_driver('firefox') ##c/drivers/gecko on the big computer
browser.implicitly_wait(15) #tells browser to wait up to 15 seconds for delay loading

browser.get('https://apps.crowdtangle.com/auth?view=0')
here_button = browser.find_element_by_css_selector('.authView__disclaimer--KNPUl > a:nth-child(3)')
here_button.click()

phone_box = browser.find_element_by_css_selector('#email')
phone_box.click()
phone_box.send_keys(phone)

pWord = browser.find_element_by_css_selector('#pass')
pWord.click()
pWord.send_keys(password)

LogIn_Button = browser.find_element_by_css_selector('#loginbutton')
LogIn_Button.click()
sleep(4)
'''
Navigating to the Historical Data page, selecting scope as "By List," selecting list as "Legacy Neutral"
'''

browser.get('https://apps.crowdtangle.com/oddashboardv4/lists/pages')
sleep(3)
Settings_button = browser.find_element_by_css_selector('.settings > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)').click()
sleep(2)

HistoricalData_Button = browser.find_element_by_css_selector('html.no-js body.facebook div.react-header-container div.react-super-inner-container div.settings div div.open ul.dropdown-menu.header-menu li a#historical-data')
HistoricalData_Button.click()
sleep(3)

ScopeDropdown_Button = browser.find_element_by_css_selector('#select_scope_chzn > a:nth-child(1) > div:nth-child(2)').click()
sleep(1)
ByList_Button = browser.find_element_by_css_selector("#select_scope_chzn_o_1").click()

'''
Initializing Custom Date range
'''

PickDates_Button = browser.find_element_by_css_selector('#select_dates_chzn > a:nth-child(1) > div:nth-child(2)')
sleep(1)
PickDates_Button.click()
sleep(1)
CustomDates_Button = browser.find_element_by_css_selector('#select_dates_chzn_o_5')
sleep(2)
CustomDates_Button.click()

'''
Main function
'''

def Fetch_PostHistory(begin, until, interval):
    """
    Takes start date, end date, and capture interval as arguments.
    Returns a csv via email containing posts for a given interval between start and end date.
    
    For interval: 'W' = weekly, 'M' = monthly, 'D' = daily.
    For begin and until: enter dates with the month, day, year format: 05/01/2020.

    """

    Capture_range = pd.date_range(start = str(begin), end = str(until), freq = str(interval)).strftime('%m/%d/%Y')
    Capture_range = Capture_range.tolist()
    
    From_Box = browser.find_element_by_css_selector('input.input-small:nth-child(1)')
    To_Box = browser.find_element_by_css_selector('input.input-small:nth-child(3)')
    FetchHistory_Button = browser.find_element_by_css_selector('.btn-primary')
    
    i = 0
    j = i + 1
    for k in range(len(Capture_range)-1):
        try:
            Start_Date = Capture_range[i]                
            End_Date = Capture_range[j]
            end_datetime = datetime.strptime(End_Date, "%m/%d/%Y")
            curr_datetime = datetime.now()
            days_between = curr_datetime - end_datetime
            
            From_Box.click()
            sleep(1)
            From_Box.clear()
            sleep(1)
            
            for char in Start_Date:
                From_Box.send_keys(char)
                sleep(.2)
            
            To_Box.click()
            sleep(1)
            To_Box.clear()
            sleep(1)
            
            for q in range(days_between.days):
                To_Box.send_keys(Keys.LEFT)
                sleep(.2)
            To_Box.send_keys(Keys.ENTER)
            
            FetchHistory_Button.click()
            
            i += 1
            j += 1
            sleep(randint(5, 10))
        
        except:
           all_lines = [i, '\n', traceback.format_exc(), '\n'] 
           errorFile = open('errorInfo_' + str(today) +'.txt', 'a') #opens file in append mode
           errorFile.writelines(all_lines)
           errorFile.close()
        
Fetch_PostHistory('04/20/2020', '05/11/2020', 'W')

browser.close()