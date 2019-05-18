'''
Created on 2019年5月18日

@author: Jennifer Shi
'''
from com.web.autotest.common.Page import Page
from selenium.webdriver.common.by import By

class BaiDuMainPage(Page):
    '''
    classdocs
          封装界面元素
    '''
    searchInput = (By.ID, 'kw')
    searchButton = (By.ID, 'su')

    def search(self, data):
        self.findElement(*self.searchInput).send_keys(data)
        self.findElement(*self.searchButton).click()
        
        