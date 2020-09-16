#coding = utf-8

#Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#DB
from pymongo import MongoClient
#Web
from selenium import webdriver
from lxml import etree
import time
from models import QQ_group
#####################################


def get_freshList(dataList):
    '处理获得的list数据,清除多余的字符'
    freshList=[]
    for i in dataList:
        freshList.append("".join(i.replace('\n','').replace(' ','').replace('\t','')))

    return freshList


class MyEmail:
    '发送邮件类'

    def send(self,you,text):
        'you接收一个list.向列表内的人发送'
        me = 'swhwtqwer@163.com'
        #you = ['741494582@qq.com']  # 联系人列表

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "My Weather"
        msg['From'] = "Wheather Python"
        msg['To'] = ",".join(you)

        # Create the body of the message (a plain-text and an HTML version).
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        #part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        #msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('smtp.163.com')
        s.set_debuglevel(True)
        s.login('swhwtqwer@163.com', '754154954582wy')    #邮箱的账户 ,密码
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()


    def send2(self,you,text):
        'you 为单个人的地址'
        s = smtplib.SMTP('smtp.163.com')
        s.set_debuglevel(True)
        s.login('swhwtqwer@163.com', '754154954582wy')
        sub = "Python_Weather"
        msg = MIMEText(text)

        msg['Subject'] = '%s' % sub
        msg['From'] = 'swhwtqwer@163.com'
        msg['To'] = you

        s.send_message(msg)
        s.quit()


class Mydb:
    'mongodb 操作类'
    def connect():
        client = MongoClient()
        db = client.Taoey
        return db

class MyWeb:

    def get_qq_group(self,user, password):

        # chromedriver = "D:\CCApplication\Mozilla Firefox\firefox.exe"
        # driver = webdriver.Firefox()
        chromedriver = "D:\CCApplication\phantomjs-2.1.1-windows\bin\phantomjs.exe"
        driver = webdriver.PhantomJS()

        driver.get("http://qun.qq.com/member.html")

        IframeElement = driver.find_element_by_name("login_frame")
        driver.switch_to_frame(IframeElement)

        driver.find_element_by_xpath("//*[@id='bottom_qlogin']/a[1]").click()  # 登录界面
        driver.find_element_by_xpath("//*[@id='u']").send_keys(user)
        driver.find_element_by_xpath("//*[@id='p']").send_keys(password)

        driver.find_element_by_xpath("//*[@id='login_button']").click()  # 点击登录
        time.sleep(2)

        driver.switch_to_default_content()  # 防止出现TypeError: can't access dead object 错误特别重要

        web_data = driver.page_source
        selector = etree.HTML(web_data)
        try:
            qq_numbers= selector.xpath("//li[@data-id]/@data-id")  # 获取所有的QQ群组号码和名称
            qq_names= selector.xpath("//li[@data-id]/@title")
            for qq_name, qq_number in zip(qq_names, qq_numbers):
                data = {
                    '_user_name': user,
                    '_name': qq_name,
                    '_num': qq_number,
                }
                db = Mydb.connect()
                db.QQ_group.insert_one(data)
        except Exception as e:
            print("QQ服务器又讨厌咱了,换个qq号或者等下再试吧")
        driver.quit()

