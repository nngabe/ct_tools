# 5/12/2020 Nick Gabriel

from time import sleep
import datetime
from os import sys, path
import os
from shutil import copy as cp
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback, logging, configparser


import numpy as np
from numpy.random import randint
import pandas as pd
from bs4 import BeautifulSoup

from ct_utils import fb_login, get_driver

def search_links(links_file, rootdir):
    rtic = lambda n: randint(1,n) # lag to simulate manual data collection

    ### get FB/CrowdTangle username and password from INI file
    config_file = path.expanduser('~/config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)
    username = config['CrowdTangle']['username']
    password = config['CrowdTangle']['password']
   
    ### selenium driver setup
    browser = 'chrome' 
    driver = get_driver(browser)
    driver.implicitly_wait(4) # doesn't work for me but may work for you

    fb_login(driver, username, password)
    driver.get('https://apps.crowdtangle.com/search/home')
    sleep(4+rtic(4))

    ### build directory structure to write data
    outdir = rootdir + 'out_search'
    if not (os.path.exists(outdir)):
        os.mkdir(outdir)
    dt_string = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    write_dir = outdir + '/' + dt_string
    os.mkdir(write_dir)
    cp(links_file,write_dir)
    
    links_df = pd.read_csv(links_file,index_col=0)
    indices = list(links_df.index)
    links = list(links_df.links)

    for idx,link in zip(indices,links):    

        search_box = driver.find_element_by_xpath('//input[starts-with(@class,"searchBar")]')
        search_box.click()
        search_box.send_keys(link)
        search_box.send_keys(Keys.ENTER)
        sleep(6+rtic(4))

        platforms = driver.find_element_by_class_name('react-tab-container').find_elements_by_tag_name('div')
        write_path = write_dir + '/' + 'link_' + str(idx)
        os.mkdir(write_path)
        df = {}
        for element in platforms:
            name = element.text
            element.click()
            sleep(2+rtic(3))
            try:
                table = driver.find_element_by_xpath('//div[starts-with(@class,"searchResultsTable")]')
            except:
                #print('no links on %s!' %name)
                continue
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
            df[name]['hrefs'] = hrefs

            spl = lambda x,delim,n: x.split(delim) if (n==0) else x.split(delim)[0:n]
            joinif = lambda arr: ''.join(arr) if (len(arr)>1) else arr[0]
            try:
                df[name]['Interactions'] = df[name]['Interactions'].apply(spl,args=[',',0]).apply(joinif)
            except:
                pass
            try:
                df[name]['Members'] = df[name]['Members'].apply(spl,args=[' ',1]).apply(spl,args=[',',0]).apply(joinif)
            except:
                pass
     
            df[name].to_csv(write_path + '/' + name +'.csv')

    driver.close()
            
if __name__ == '__main__':

    rootdir = './'
    links_file = 'links.csv'
    search_links(links_file, rootdir)

