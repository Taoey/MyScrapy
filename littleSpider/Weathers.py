import requests,time
from lxml import etree
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver


url_cz='http://www.weather.com.cn/weather1d/101090701.shtml#around1'
url_qhd='http://www.weather.com.cn/weather1d/101091101.shtml#input'
url_xi_an='http://www.weather.com.cn/weather1d/101110101.shtml#input'

class Weather():
    '天气类'
    def __init__(self):
        self.today_time=""
        self.today_weather=""
        self.today_T=""
        self.tomorrow_time=""
        self.tomorrow_weather=""
        self.tomorrow_T=""


    def get_weather(self,url):
        '获得天气数据'
        req=requests.get(url)
        req.encoding = 'utf-8'

        selector=etree.HTML(req.text)

        self.place=selector.xpath("//div[@class='crumbs fl']/a[2]/text()")[0]
        self.today_time=selector.xpath("//*[@id='today']/div[2]/ul/li[1]/h1/text()")[0]
        self.today_weather=selector.xpath("//*[@id='today']/div[2]/ul/li[1]/p[1]/text()")[0]
        self.today_T=selector.xpath("//*[@id='today']/div[2]/ul/li[1]/p[2]/span/text()")[0]+"℃"
        self.tomorrow_time=selector.xpath("//*[@id='today']/div[2]/ul/li[2]/h1/text()")[0]
        self.tomorrow_weather=selector.xpath("//*[@id='today']/div[2]/ul/li[2]/p[1]/text()")[0]
        self.tomorrow_T=selector.xpath("//*[@id='today']/div[2]/ul/li[2]/p[2]/span/text()")[0]+"℃"

    def print(self):
        '打印天气数据到控制台'
        print(self.place)
        print(self.today_time,self.today_weather,self.today_T)
        print(self.tomorrow_time,self.tomorrow_weather,self.tomorrow_T)

class MyEmail():
    '发送邮件类'
    def sendEmail(self,you,text):
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
               Here is美丽e <a href="https://www.python.org">link</a> you wanted.
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


    def sendEmail2(self,you,text):
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


    def sendEmail3(self,you,text):
        # chromedriver = "D:\CCApplication\Mozilla Firefox\firefox.exe"
        # driver = webdriver.Firefox()

        chromedriver = "D:\CCApplication\phantomjs-2.1.1-windows\bin\phantomjs.exe"
        driver = webdriver.PhantomJS()

        driver.get("http://mail.163.com/")
        IframeElement = driver.find_element_by_id("x-URS-iframe")
        driver.switch_to_frame(IframeElement)


        driver.find_element_by_xpath("//form[@id='login-form']/div/div[1]/div[2]/input").send_keys("swhwtqwer")
        driver.find_element_by_xpath("//form[@id='login-form']/div/div[3]/div[2]/input[2]").send_keys("754154954582qq")
        driver.find_element_by_xpath("//a[@id='dologin']").click()

        driver.switch_to_default_content()  # 防止出现TypeError: can't access dead object 错误特别重要


        web_data = driver.page_source
        print(web_data)

        driver.find_element_by_id("_mail_component_70_70").click()




if __name__ == '__main__':
    one_day=60*60*24
    time.sleep(60*60*9)
    while True:
        me='741494582@qq.com'
        huanyk='2959495325@qq.com'

        urls=[url_qhd,url_cz,url_xi_an]       #地点集合
        address = [me]                          #收件人
        text=""
        e=MyEmail()                           #调用邮箱发送对象
        for i in  urls:
            w = Weather()
            w.get_weather(i)
            w.print()
            text+= "{}\n{} \n {} {} \n{} \n{} {}\n\n\n ".format(w.place,w.today_time,w.today_weather,w.today_T,w.tomorrow_time,w.tomorrow_weather,w.tomorrow_T)

            time.sleep(2)
        print(text)
        e.sendEmail(address,text)
        e.sendEmail(address[0],text)
        time.sleep(one_day)