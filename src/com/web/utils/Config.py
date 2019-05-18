'''
Created on 2019年4月20日

@author: Jennifer Shi
'''
"""
读取配置。这里配置文件用的yaml，需在FileReader中添加相应的Reader进行处理。
"""
import os
from com.web.utils.FileReader import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'conf.yaml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join((BASE_PATH + '/../../..'), 'log')
REPORT_PATH = os.path.join((BASE_PATH + '/../../..'), 'report')

class Config(object):
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data
        
    def get(self, element, index=0):
        return self.config[index].get(element)
        