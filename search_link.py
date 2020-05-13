# 5/12/2020 Nick Gabriel

from time import sleep

from os import sys, path
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback, logging, configparser


import numpy as np
from numpy.random import randint
import pandas as pd
from bs4 import BeautifulSoup

from ct_utils import fb_login, get_driver

if __name__ == '__main__':

    rtic = lambda n: randint(1,n)
    config = configparser.ConfigParser()
    config.read(path.expanduser('~/config.ini'))

    username = config['CrowdTangle']['username']
    password = config['CrowdTangle']['password']
    
    link = 'https://www.nature.com/articles/d41586-020-01095-0'
    browser = 'chrome'
    driver = get_driver(browser)
    driver.implicitly_wait(4) # doesn't work for me but may work for you

    fb_login(driver, username, password)
    driver.get('https://apps.crowdtangle.com/search/home')
    sleep(4+rtic(3))

    xpath = '//*[@id="react-search"]/div[2]/div[2]/form/div[1]/div[2]/label/input'
    search_box = driver.find_element_by_xpath(xpath)
    search_box.click()
    search_box.send_keys(link)
    search_box.send_keys(Keys.ENTER)
    sleep(6+rtic(3))

    xpath = '//*[@id="react-search"]/div[2]/div[2]/div/div[2]/div'
    platforms = driver.find_element_by_xpath(xpath).find_elements_by_tag_name('div')

    df = {}
    for element in platforms:
        name = element.text
        element.click()
        
        xpath = '//*[@id="react-search"]/div[2]/div[2]/div/div[3]/div/div[2]'
        table = driver.find_element_by_xpath(xpath)
        source = table.get_attribute('outerHTML')
        soup = BeautifulSoup(source, 'html.parser')
        m = len(soup.find_all('a'))
        hrefs = [soup.find_all('a')[i].get('href') for i in range(m) ]

        text = [soup.find_all('p')[i].text for i in range(m*5) ]
        cols = text[0:5]
        rows = [text[5*i:(5*(i+1))] for i in range(1,m)]

        cols[0] = 'Page'
        cols.insert(1,'Members')
        cols = cols[0:5]

        df[name] = pd.DataFrame(rows, columns=cols)

        spl = lambda x,delim,n: x.split(delim) if (n==0) else x.split(delim)[0:n]
        joinif = lambda arr: ''.join(arr) if (len(arr)>1) else arr[0]
        try:
            df[name]['Interactions'] = df[name]['Interactions'].apply(spl,args=[',',0]).apply(joinif)
        except:
            pass
        df[name]['Members'] = df[name]['Members'].apply(spl,args=[' ',1]).apply(spl,args=[',',0]).apply(joinif)

