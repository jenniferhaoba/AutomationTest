from selenium import webdriver
from com.web.utils.Config import DRIVER_PATH,REPORT_PATH
import time
import os
from com.web.utils.Log import logger


CHROMEDRIVER_PATH = DRIVER_PATH +'\chromedriver.exe'
IEDRIVER_PATH = DRIVER_PATH + '\IEDriverServer.exe'
PHANTOMJSDRIVER_PATH = DRIVER_PATH + '\phantomjs.exe'

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie, 'phantomjs': webdriver.PhantomJS}
EXECUTABLE_PATH = {'firefox': 'wires', 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH, 'phantomjs': PHANTOMJSDRIVER_PATH}

class UnSupportBrowserTypeError(Exception):
    pass

# 可根据需要扩展
class Browser(object):
    def __init__(self, browser_type = 'chrome'):
        self._type = browser_type.lower()#将参数中所有大写字母转换为小写
        if self._type in TYPES:          #遍历字典中的key
            self.browser = TYPES[self._type]
        else:
            raise UnSupportBrowserTypeError('仅支持%s！' % ','.join(TYPES.keys()))
        self.driver = None
        
    def get(self, url, maxmize_window=True, implicitlyWait=30):
        driverPath = EXECUTABLE_PATH[self._type]
        logger.info("driver path:" + str(driverPath))
        self.driver = self.browser(executable_path = driverPath)
        self.driver.get(url)
        if maxmize_window:
            self.driver.maxmize_window()
        self.driver.implicitly_wait(implicitlyWait)
        return self
    
    def saveScreenShot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = REPORT_PATH +'\screenshot_%s'% day
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
            
        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '\\%s_%s.png'%(name, tm))
        return screenshot
    def close(self):
        self.driver.close()
    def quit(self):
        self.driver.quit()
                       
        
        