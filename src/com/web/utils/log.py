"""
日志类。通过读取配置文件，定义日志级别、日志文件名、日志格式等。
日志级别等级CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
一般直接把logger import进去
from utils.log import logger
logger.info('test log')
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from com.web.utils.Config import LOG_PATH, Config
import os

class Logger(object):
    def __init__(self, logger_name='AutoTestlog'):
        self.logger = logging.getLogger(logger_name) 
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        #config文件中log配置不为空时取配置文件否则取‘test.log’
        self.log_file_name = c.get('file_name') if c and c.get('file_name') else 'test.log'
        # 保留的日志数量
        self.backup_count = c.get('backup_count') if c and c.get('backup_count') else 7
        
        self.console_output_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_output_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)
        
    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
                            这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
                            两个句柄的日志级别不同，在配置文件中可设置。
        """
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)
            
            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1, # one week
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger
    
loggerUtils = Logger()    #类方法不能直接调用，先实例化对象再调用
logger = loggerUtils.get_logger()