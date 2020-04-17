import datetime
import time 

from os import sys, path
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy as np
from numpy.random import randint
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

  time.sleep(8)

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



def update_list(uids, driver, ct_url, action):

  """
  Add pages to a Crowdtangle list using their uids.

  Params:
  uids (list of str)
  driver (WebDriver)
  password (str)

  Returns:
  none
  """
  
  if action in ['add','a', 1]:
    button_sign = 'fas fa-plus'
  if action in ['remove', 'r', 0]:
    button_sign = 'fas fa-minus'


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
  try:
    xpath = '//*[@id="manage-lists-nav"]/li[2]/a'
    search_tab = driver.find_element_by_xpath(xpath)
    search_tab.click()
    time.sleep(4)
  except:
    print('cant go to Manage tab. Already there?')

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
      if (sign.get_attribute('class')==button_sign):
        button.click()
        print('success: ',uid)
      else:
        print('already in list: ',uid)
    except Exception as e:
      print('failed: ',uid)

    time.sleep(2)
    search_box.clear()
    time.sleep(2)



def grab_posts(uids, driver, ct_url):
  
  """
  Request post data from crowtangle from uid list 

  Params:
  uids (list of str)
  driver (WebDriver)
  password (str)

  Returns:
  none
  """
  ### navigate to page
  url = ct_url
  driver.get(url)
  time.sleep(8)

  # find Manage tab and click, xpath changes sometimes...
  manage_paths = ['//*[@id="ui-id-4"]/span','//*[@id="ui-id-14"]/span']
  for xpath in manage_paths:
    try:
      manage_tab = driver.find_element_by_xpath(xpath)
      manage_tab.click()
      time.sleep(4)
      break
    except:
      time.sleep(2)
      pass
  i = 1
  n = len(uids)
  for uid in uids:

    print('--------------------')
    print('attempting %i/%i: %s' % (i,n,uid))
    i += 1 

    ### add page
    try:
      xpath = '//*[@id="manage-lists-nav"]/li[2]/a'
      search_tab = driver.find_element_by_xpath(xpath)
      search_tab.click()
      time.sleep(3)
    except:
      print('cant go to Add page tab. Already there?')

    # go to search box and search uid
    xpath = '//*[@id="add-producers-container"]/div/div/div[1]/div/input'
    search_box = driver.find_element_by_xpath(xpath)
    time.sleep(3)

    search_box.click()
    search_box.send_keys(uid)
    search_box.send_keys(Keys.ENTER)
    time.sleep(6)

    # check status and add page if not added yet
    try:
      xpath = '//*[@id="add-producers-container"]/div/div/div[2]/div/div/div[2]/button'
      sign = driver.find_element_by_xpath(xpath + '/i')
      button = driver.find_element_by_xpath(xpath)
      if (sign.get_attribute('class')=='fas fa-plus' ):
        button.click()
        print('success: ',uid)
      else:
        print('already in list: ',uid)
    except:
      pass

    time.sleep(2)

    ### download data
    xpath = '//*[@id="manage-lists-nav"]/li[1]/a'
    view_tab = driver.find_element_by_xpath(xpath)
    view_tab.click()
    time.sleep(4)
    try:
      xpath = '/html/body/div[3]/div/div[3]/div/div/div[2]/div[2]/div[4]/div/div[2]/div/ul/li/ul/li/div[2]/div/span[1]/a'
      download_button = driver.find_element_by_xpath(xpath)
      download_button.click()
      time.sleep(4) 
      submit = driver.find_element_by_xpath('//*[@id="submit_button"]')
      submit.click()
      time.sleep(4)
    except:
      pass
    
    clear_list(driver)

    ### remove page
    xpath = '//*[@id="manage-lists-nav"]/li[2]/a'
    search_tab = driver.find_element_by_xpath(xpath)
    search_tab.click()
    time.sleep(4) 

    # go to search box and search uid
    try:
      xpath = '//*[@id="add-producers-container"]/div/div/div[1]/div/input'
      search_box = driver.find_element_by_xpath(xpath)
      time.sleep(4)

      search_box.click()
      search_box.send_keys(uid)
      search_box.send_keys(Keys.ENTER)
      time.sleep(6)
    except:
      pass
    # check status and add page if not added yet
    try:
      xpath = '//*[@id="add-producers-container"]/div/div/div[2]/div/div/div[2]/button'
      sign = driver.find_element_by_xpath(xpath + '/i')
      button = driver.find_element_by_xpath(xpath)
      if (sign.get_attribute('class')=='fas fa-minus'):
        button.click()
        print('success: ',uid)
      else:
        print('already in list: ',uid)
    except:
      pass

    time.sleep(2)
    try:
      search_box.clear()
    except:
      pass
    time.sleep(4)

def clear_list(driver):

  try:
    xpath = '//*[@id="manage-lists-nav"]/li[1]/a'
    view_tab = driver.find_element_by_xpath(xpath)
    view_tab.click()
    time.sleep(4)
  except:
    pass

  for i in range(1,10):
    try:
      xpath = '/html/body/div[3]/div/div[3]/div/div/div[2]/div[2]/div[4]/div/div[2]/div/ul/li[' + str(i) + ']/ul/li/div[2]/div/a'
      remove_button = driver.find_element_by_xpath(xpath)
      remove_button.click()
      time.sleep(1)
      xpath = '/html/body/div[3]/div/div[3]/div/div/div[2]/div[2]/div[4]/div/div[2]/div/ul/li[' + str(i) + ']/ul/li/div[2]/div/div/a[1]'
      remove_confirm = driver.find_element_by_xpath(xpath)
      remove_confirm.click()
      time.sleep(1)
    except:
      break 

if __name__ == '__main__':

  uids = list(pd.read_csv('~/vax_new.tsv','\t').loc[:,'fb_uid'].astype(str))[862:]
  dummies = ['230114651240','110844299008350','147555688654796']
  ct_url = 'https://apps.crowdtangle.com/iddptest/lists/1364653'
  fb_username = pd.read_csv('~/cred.csv').iloc[0,0]
  fb_password = pd.read_csv('~/cred.csv').iloc[1,0]
  #fb_username = 'name@email.com' 
  #fb_password = 'password'

  driver = get_driver()
  fb_login(driver, fb_username, fb_password)
  
  update_list(dummies, driver, ct_url, 'remove')
  print('dummy pages removed...')
  
  grab_posts(uids,driver, ct_url)
  print('downloaded posts...')
  
  update_list(dummies, driver, ct_url, 'add')
  print('dummy pages restored...')

  print('closing driver...')
  driver.close()



