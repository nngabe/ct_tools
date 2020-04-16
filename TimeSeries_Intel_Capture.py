# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:57:21 2020

@author: Rhys Leahy © 
"""

##Script to automate collecting intelligence from CrowdTangle

##Step 1. Get list of page ids from elements in a CT Leaderboard and save as Leaderboard_Ids.csv
##Step 2. Load the csv at line 64 and check that everything transferred
##Step 3. Enter phone number and password for the fb account needed to access CT
##Step 4. Check the date range in browser.get() in main function-- make sure the end date goes until today and URL has correct interval
##Step 5. Run this script



from time import sleep
from random import randint
from selenium import webdriver
import traceback, logging
import pandas as pd

logging.basicConfig(filename= 'CT_Intel_ProgramLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of program')

browser = webdriver.Firefox(executable_path = 'C:\Program Files\geckodriver.exe') ##change path according to gecko executable on different computers
browser.implicitly_wait(15) #tells browser to wait up to 15 seconds for delay loading

'''
Block loads and logs in to CrowdTangle
'''

browser.get('https://apps.crowdtangle.com/auth?view=0')
here_button = browser.find_element_by_css_selector('.authView__disclaimer--KNPUl > a:nth-child(3)')
here_button.click()

phone_box = browser.find_element_by_css_selector('#email')
phone_box.click()
phone_box.send_keys('')

pWord = browser.find_element_by_css_selector('#pass')
pWord.click()
pWord.send_keys('')

LogIn_Button = browser.find_element_by_css_selector('#loginbutton')
LogIn_Button.click()

'''
Function takes the id of a a fan page on crowd tangle, navigates to the page Intel, 
and exports a CSV of the % likes growth over date specified in the URL. Dates in URL need to be modified for desired timeframe.  
'''

def getPageLikesIntel(Pg_id):
        browser.get('https://apps.crowdtangle.com/oddahsboardtest01/reporting/intelligence?accountType=facebook_page&accounts=' + Pg_id + '&brandedContentType=none&comparisonType=none&endDate=2020-03-04T23%3A59%3A59&followersBreakdownType=pageLikes&followersShowByType=total&graphType=subscriber_count&interval=week&platform=facebook&reportTimeframe=custom&startDate=2018-06-01T00%3A00%3A00')
        elem = browser.find_element_by_css_selector('.all-export-icons > span:nth-child(3)')
        sleep(randint(2, 10))
        elem.click()
        
'''
Creates a df of page ids from a CrowdTangle list. To obtain this list, need to scrape the ids from Leaderboard and save as CSV.
This also converts each element in the list to a string.
'''
df = pd.read_csv('Leaderboard_ids.csv', delimiter = ',') 
Leaderboard_pages = df['CT_id'].to_list()
for i in range(0, len(Leaderboard_pages)): 
    Leaderboard_pages[i] = str(Leaderboard_pages[i]) 
    
'''
This block loops through all of the CT_ids loaded from the df to dem_pages and calls the main function
'''

for i in Leaderboard_pages:
   Page = i
   try: 
       getPageLikesIntel(Page)
       sleep(randint(2,20))
   except:
       all_lines = [i, '\n', traceback.format_exc(), '\n'] 
       errorFile = open('errorInfo_Leaderboard.txt', 'a') #opens file in append mode
       errorFile.writelines(all_lines)
       errorFile.close()
   

browser.close() ##Closes out of firefox
