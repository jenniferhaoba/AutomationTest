'''
Created on 2019年4月20日

@author: Jennifer Shi
'''
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class BaiDuTest(unittest.TestCase):
    
    URL = "https://www.baidu.com/"
    base_path = os.path.dirname(os.path.abspath(__file__)) + '\..'
    driver_path = os.path.abspath(base_path + '\drivers\chromedriver.exe')
    
    searchBox = (By.ID, 'kw')
    searchButton = (By.ID, 'su')
    result = (By.XPATH, '//div[contains(@class, "result")]/descendant::a[1]')
        
    def setUp(self):
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.get(self.URL)
        
    def tearDown(self):
        self.driver.quit()
        
    def testSearch(self):
        self.driver.find_element(*self.searchBox).send_keys('selenium')
        self.driver.find_element(*self.searchButton).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.result)
        for link in links:
            print(link.text)
        
if __name__ == '__main__':
    unittest.main()
    
 
    
    