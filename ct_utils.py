import datetime
import time 

from os import sys, path
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy as np
import pandas as pd



def fb_login(driver,username,password):
  
  """Login to Facebook (also granting access to crowdtangle)"""  

  url = 'https://www.facebook.com/' 
  driver.get(url)
  
  try:
    id_box = driver.find_element_by_name('email')
  except:
    id_box = driver.find_element_by_xpath('//*[@id="email"]')
  id_box.send_keys(username)

  pass_box = driver.find_element_by_name('pass')
  pass_box.send_keys(password)
  
  pass_box.send_keys(Keys.RETURN)

  time.sleep(4)

def get_driver():
  
  """Initialize driver with whatever options you want here."""

  options = Options()
  
  #options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-notifications')
  options.add_argument('--disable-gpu')
  options.add_argument('start-maximized')
  options.add_argument('disable-infobars')
  options.add_argument('--disable-extensions')
  options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options=options)

  return driver


def update_list(uids, driver, ct_url):

  """
  Add pages to a Crowdtangle list using their uids.

  Params:
  uids (list of str)
  driver (WebDriver)
  password (str)

  Returns:
  none
  """
  
  url = ct_url
  driver.get(url)
  time.sleep(8)

  # find manage tab and click, xpath changes sometimes...
  manage_paths = ['//*[@id="ui-id-4"]/span','//*[@id="ui-id-14"]/span']
  for xpath in manage_paths:
    try:
      manage_tab = driver.find_element_by_xpath(xpath)
      manage_tab.click()
      time.sleep(4)
      break
    except:
      time.sleep(4)
      pass

  # go to Manage tab
  xpath = '//*[@id="manage-lists-nav"]/li[2]/a'
  search_tab = driver.find_element_by_xpath(xpath)
  search_tab.click()
  time.sleep(4) 

  # go to Add Pages tab
  xpath = '//*[@id="add-producers-container"]/div/div/div[1]/div/input'
  search_box = driver.find_element_by_xpath(xpath)
  time.sleep(2)
 
  # indices for progress updates
  i = 1
  n = len(uids) 
  for uid in uids: 
    
    print('--------------------')
    print('attempting %i/%i: %s' % (i,n,uid))
    i += 1 
    ### navigate to CrowdTangle search page and search for group 
    # search page
    search_box.click()
    search_box.send_keys(uid)
    search_box.send_keys(Keys.ENTER)
    time.sleep(4)

    try:
      xpath = '//*[@id="add-producers-container"]/div/div/div[2]/div/div/div[2]/button'
      sign = driver.find_element_by_xpath(xpath + '/i')
      button = driver.find_element_by_xpath(xpath)
      # click box if it hasn't been added yet
      if (sign.get_attribute('class')=='fas fa-plus'):
        button.click()
        print('added: ',uid)
    except Exception as e:
      print('failed: ',uid)

    time.sleep(2)
    search_box.clear()
    time.sleep(4)


def grab_posts(uids, driver, ct_url)
  
  """
  Request post data from crowtangle from uid list 

  Params:
  uids (list of str)
  driver (WebDriver)
  password (str)

  Returns:
  none
  """

  # add uid
  # download data
  # remove uid


  return 0
    

if __name__ == '__main__':

  #uids = list(pd.read_csv('vax_new.tsv','\t').loc[:,'fb_uid'].astype(str))[0:3]
  uids = ['230114651240','110844299008350','147555688654796']
  ct_url = 'https://apps.crowdtangle.com/iddptest/lists/1364653'
  fb_username = pd.read_csv('~/cred.csv').iloc[0,0]
  fb_password = pd.read_csv('~/cred.csv').iloc[1,0]
  #fb_username = 'name@email.com' 
  #fb_password = 'password'

  driver = get_driver()
  fb_login(driver, fb_username, fb_password)
  update_list(uids, driver, ct_url)



