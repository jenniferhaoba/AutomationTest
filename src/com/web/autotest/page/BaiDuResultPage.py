'''
Created on 2019年5月18日

@author: Jennifer Shi
'''
from com.web.autotest.page.BaiDuMainPage import BaiDuMainPage
from selenium.webdriver.common.by import By

class BaiDuResultPage(BaiDuMainPage):
    '''
    搜索结果页
    '''
    result = (By.XPATH, '//div[contains(@class, "result")]/descendant::a[1]')
    
    @property
    def resultLinks(self):
        elements = self.findElements(*self.result)
        return elements
        
        