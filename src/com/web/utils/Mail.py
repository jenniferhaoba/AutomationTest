'''
Created on 2019年4月20日

@author: Jennifer Shi
'''
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from socket import gaierror, error
import time
from smtplib import SMTPResponseException, SMTPAuthenticationError
from com.web.utils.Log import logger


"""
邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
Content-disposition 是 MIME 协议的扩展，MIME 协议指示 MIME 用户代理如何显示附加的文件
Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
当你在响应类型为application/octet- stream情况下使用了这个头信息的话，那就意味着你不想直接显示内容，而是弹出一个”文件下载”的对话框，接下来就是由你来决定“打开”还是“保存” 了
使用MIMEMultipart发送多个附件的邮件
发送HTML格式的邮件与发送纯文本消息的邮件不同之处就是将MIMEText中_subtype设置为html或plain

"""
class Email:
    def __init__(self, server, port, sender, password, receiver, title, message=None, path=None):
        """初始化Email

    :param title: 邮件标题，必填。
    :param message: 邮件正文，非必填。
    :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
    :param server: smtp服务器，必填。
    :param sender: 发件人，必填。
    :param password: 发件人密码，必填。
    :param receiver: 收件人，多收件人用“；”隔开，必填。
    """
        self.title = title
        self.message = message
        self.files = path
        
        self.msg = MIMEMultipart('related')#采用related定义内嵌资源的邮件体
        self.server = server
        self.password = password
        self.receiver = receiver
        self.sender = sender
        self.port = port
        
    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' %att_file, 'rb').read(), 'plain', 'utf-8')##_subtype有plain,html等格式    
        att["Content-Type"] = 'application/octet-stream'#request header内容设置，上传附件类型设置，该类型可以上传多种附件图片，视频，文件等
        file_name = re.split(r'[\\|/]', att_file) #按正则表达式设置的模式分隔附件
        #打开文件时需要提示用户保存，就要利用header中Content-Disposition进行一下处理
        #filename参数可以包含路径信息，但User-Agnet会忽略掉这些信息，只会把路径信息的最后一部分做为文件名file_name[-1]
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file{}'.format(att_file))
    
    def send(self):
        self.msg['Subject'] = self.title
        self.msg['from'] = self.sender
        self.msg['To'] = self.receiver
        
        #邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))#attach new subparts to the message by using the attach() method
        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)
        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP_SSL(self.server)# 连接sever
            smtp_server.connect(self.server, self.port)
        except (gaierror, error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)# 登录
                time.sleep(5)
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())# 发送邮件
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))
            except SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            except SMTPResponseException as e :
                logger.exception("send exception:%s", str(e))

            finally:
                smtp_server.quit()# 断开连接
                
             
        
        
        
        
        
       
