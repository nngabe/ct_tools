# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:07:39 2020

@author: rhysl
"""


##Script to automate collecting historical posts at different intervals from CrowdTangle

from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import date, time
import pandas as pd
import traceback, logging, configparser


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

browser = webdriver.Firefox(executable_path = 'C:\Program Files\geckodriver.exe') ##c/drivers/gecko on the big computer
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

'''
Navigating to the Historical Data page, selecting scope as "By List," selecting list as "Legacy Neutral"
'''

browser.get('https://apps.crowdtangle.com/oddahsboardtest01/lists/pages')
sleep(3)
Settings_button = browser.find_element_by_css_selector('.settings > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)').click()
sleep(2)

HistoricalData_Button = browser.find_element_by_css_selector('html.no-js body.facebook div.react-header-container div.react-super-inner-container div.settings div div.open ul.dropdown-menu.header-menu li a#historical-data')
HistoricalData_Button.click()
sleep(3)

ScopeDropdown_Button = browser.find_element_by_css_selector('#select_scope_chzn > a:nth-child(1) > div:nth-child(2)').click()
sleep(1)
ByList_Button = browser.find_element_by_css_selector("#select_scope_chzn_o_1").click()


PagesDropdown_Button = browser.find_element_by_css_selector('#sel9W3_chzn').click()
sleep(1)

##struggling to select dropdown choice below
mySelectElement = browser.find_element_by_css_selector('#sel9W3')
dropDownMenu = Select(mySelectElement)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[3]/div/div/form/section[1]/div[2]/select/optgroup[1]")))
dropDownMenu.select_by_visible_text('kor_vax')

#css selector for list of pages optgroup.select-option:nth-child(1) 
#css selector for KOR vax optgroup.select-option:nth-child(1) > option:nth-child(13)


browser.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/form/section[1]/div[2]/select/optgroup[1]/option[13]')
#xpath kor vax /html/body/div[3]/div/div[3]/div/div/form/section[1]/div[2]/select/optgroup[1]/option[13]



'''
Initializing Custom Date range
'''

PickDates_Button = browser.find_element_by_css_selector('#select_dates_chzn > a:nth-child(1) > div:nth-child(2) > b:nth-child(1)').click()
sleep(1)
CustomDates_Button = browser.find_element_by_css_selector('html.no-js body.facebook div#body-container div#body-container-inner div#content.full div#primary.primary div.historical-container form#historical-data-form section.historical-step div.historical-step-field div#select_dates_chzn.chzn-container.chzn-container-single.chzn-container-single-nosearch div.chzn-drop ul.chzn-results li#select_dates_chzn_o_5.active-result.result-selected').click()

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
            From_Box.clear()
            From_Box.send_keys(Start_Date, Keys.ENTER)
            sleep(3)
            To_Box.clear()
            To_Box.send_keys(End_Date, Keys.ENTER)
            sleep(3)
            FetchHistory_Button.click()
            i += 1
            j += 1
            sleep(randint(5, 10))
        except:
           pass
    #        all_lines = [i, '\n', traceback.format_exc(), '\n'] 
    #        errorFile = open('errorInfo_' + str(today) +.txt', 'a') #opens file in append mode
    #        errorFile.writelines(all_lines)
    #        errorFile.close()
        
Fetch_PostHistory('12/01/2019', '01/01/2020', 'W')

# browser.close()




FetchHistory_Button = browser.find_element_by_css_selector('.btn-primary').click()
    
#send keys of recent and older date

#Fetch history for those dates
#Wait

#Recent_Date = older date
#Older date = older_date month - 3












   

browser.close() ##Closes out of firefox



















# # Then we need a loop to work with
# import asyncio

# loop = asyncio.get_event_loop()

# # We also need something to run
# async def main():
#     for char in 'Hello, world!\n':
#         print(char, end='', flush=True)
#         await asyncio.sleep(randint(1, 499)/1000)

# ##muaha a way to send keys with extremely human like behavior

# # Then, we need to run the loop with a task
# loop.run_until_complete(main())



    
