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
    username = 'nickgabriel8' #config['CrowdTangle']['username']
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
        
        ### clear search box
        try:
            clear_button = driver.find_element_by_xpath('//div[starts-with(@class,"searchBar__clearBtn")]')
            clear_button.click()
        except:
            pass
        
        ### entering a new search 
        search_box = driver.find_element_by_xpath('//input[starts-with(@class,"searchBar")]')
        search_box.click()
        search_box.send_keys(link)
        search_box.send_keys(Keys.ENTER)
        #return driver
        sleep(6+rtic(4))

        download_button = driver.find_element_by_xpath('//div[starts-with(@class,"searchOptions__optionBtnContainer")]')
        download_button.click()    
    
    return download_button
    #driver.close()
            
if __name__ == '__main__':

    rootdir = './'
    links_file = 'keywords.csv'
    download_button = search_links(links_file, rootdir)

