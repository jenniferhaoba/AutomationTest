from com.web.autotest.common.Browser import Browser
from com.web.utils.log import logger

class Page(Browser):
    '''
          页面公共用法操作封装
    '''
    def __init__(self, page=None, browser_type='chrome'):
        if page:
            self.driver = page.driver
        else:
            super().__init__(browser_type=browser_type)#super() 函数是用于调用父类(超类)的一个方法
    def getDriver(self):
        return self.driver
    
    def findElement(self, *args):
        element = self.driver.find_element(*args)
        return element
    
    def findElements(self, *args):
        return self.driver.find_elements(*args)  
            
            
    