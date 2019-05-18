'''
Created on 2019年4月20日

@author: Jennifer Shi
'''
import time
import unittest
#from selenium import webdriver
#from selenium.webdriver.common.by import By
from com.web.utils.Config import Config, DRIVER_PATH, REPORT_PATH
from com.web.utils.log import logger
from com.web.utils.HTMLTestRunner import HTMLTestRunner
import os
from com.web.utils.mail import Email
from com.web.autotest.page.BaiDuResultPage import BaiDuMainPage, BaiDuResultPage


class BaiDuTestCase(unittest.TestCase):
    
    URL = Config().get('URL')
    page = None
        
    def subSetUp(self):
        # 初始页面是main page，传入浏览器类型打开浏览器
        self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maxmize_window=False)
        
    def subTearDown(self):
        self.page.quit()
        
    def testSearch(self):
        self.subSetUp()
        self.page.search('Selenium')
        time.sleep(3)
        self.page = BaiDuResultPage(self.page)# 页面跳转到result page
        links = self.page.resultLinks
        for link in links:
            logger.debug(link.text)
        self.subTearDown()
        
if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    reportName = now + '_report.html'
#   report = REPORT_PATH + "/" + str(reportName)#路径名和文件名合并用'/'和'+'
#   report = REPORT_PATH +'/%s'% reportName
    report = os.path.join(REPORT_PATH, reportName) 
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='WebAutoTest', description='')
        runner.run(BaiDuTestCase('testSearch'), True)#添加isShowChart开关，默认false不显示饼图
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
    
    
 
    
    