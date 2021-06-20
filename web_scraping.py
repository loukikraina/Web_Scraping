# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 00:37:11 2021

@author: LOUKIK RAINA
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



#path to your geckodriver
driver = webdriver.Firefox(executable_path = 'C:\\Users\\LOUKIK RAINA\\Downloads\\geckodriver-v0.29.1-win64\\geckodriver.exe')
driver.get("https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi")


def get_details(driver,result):
    elems = driver.find_elements_by_css_selector('.filter-property-list')
    elems[0].find_element_by_css_selector('a').get_attribute('href')
    elems[0].get_attribute('detailurl')
    
    for x in elems:
        d1 = {}
        temp = 0
        det = x.text
        det = det.split('\n')
        print(det)
        if len(det)==16:
            temp = -1
        d1['Apartment Size'] = det[0].split('Apartment')[0].strip()
        d1['Address'] = det[1]
        d1['Total price'] = det[2].split('@')[0].strip()
        d1['Per Sq Yd. price'] = det[2].split('@')[1].split('/')[0]
        d1['Area (Sq Yd.)'] = det[5+temp].split(' ')[0]
        d1['Facing'] = det[7+temp]
        d1['Status'] = det[9+temp]
        d1['Floor'] = det[10+temp]
        d1['Furnishing'] = det[11+temp]
        d1['Hold type'] = det[12+temp]
        d1['# of Bathroom'] = det[13+temp].split(' ')[0]
        if temp == -1: d1["Featured"]='No'
        else:d1["Featured"]='Yes'
        d1['Posted By'] = det[14+temp]
        d1['Posted'] = det[15+temp].split(':')[1].strip()
        d1['Map Url'] = x.find_element_by_css_selector('a').get_attribute('href')
        d1['Details Url'] = x.get_attribute('detailurl')
        
        
        result.append(d1)
    return result

# for current page

for z in range(2):
    
    result = []
    
    # for 3 and 4 bhk
    if z==1:
        driver.refresh()
        time.sleep(5)
        ele = driver.find_element_by_css_selector('.bd')
        ele.send_keys(Keys.RETURN)
        for x in range(3,5):
            e = driver.find_element_by_xpath(f"//input[@id='{x}']/./..")
            e.click()
            time.sleep(3)
        
    
    SCROLL_PAUSE_TIME = 2
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        
        result = get_details(driver,result)
        
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    
    df = pd.DataFrame(result)
    df = df.drop_duplicates()
    df.to_excel(f'output{z+1}.xlsx',index = False)
    
    
    
driver.close()
        
        
    















