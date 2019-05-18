'''
Created on 2019年4月20日

@author: Jennifer Shi
'''
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from com.web.utils.Config import Config, DRIVER_PATH, REPORT_PATH
from com.web.utils.log import logger
from com.web.utils.HTMLTestRunner import HTMLTestRunner
import os
from com.web.utils.mail import Email

class BaiDuTest(unittest.TestCase):
    
    URL = Config().get('URL')
    
    searchBox = (By.ID, 'kw')
    searchButton = (By.ID, 'su')
    result = (By.XPATH, '//div[contains(@class, "result")]/descendant::a[1]')
        
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + '\chromedriver.exe')
        self.driver.get(self.URL)
        
    def tearDown(self):
        self.driver.quit()
        
    def testSearch(self):
        self.driver.find_element(*self.searchBox).send_keys('selenium1')
        self.driver.find_element(*self.searchButton).click()
        time.sleep(3)
        links = self.driver.find_elements(*self.result)
        for link in links:
            logger.debug(link.text)
        
if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    reportName = now + '_report.html'
 #   report = REPORT_PATH + "/" + str(reportName)#路径名和文件名合并用/和+
    report = os.path.join(REPORT_PATH, reportName) 
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='WebAutoTest', description='')
        runner.run(BaiDuTest('testSearch'), True)#添加isShowChart开关，默认false不显示饼图
    e = Email(title='百度搜索测试报告',
              message= '这是今天的报告，请查收',
              receiver= 'jenniferhaoba@163.com',
              server='smtp.qq.com',
              port='465',
              sender='620765883@qq.com',
              password='kaypiiztiyjzbfdd',
              path=report
              )
    e.send()
    
    
 
    
    