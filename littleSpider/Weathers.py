import requests,time
from lxml import etree
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        #text = "{} \n {} {} \n{}{} {} ".format(self.today_time,self.today_weather,self.today_T,self.tomorrow_time,self.tomorrow_weather,self.tomorrow_T)
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
        s.login('swhwtqwer@163.com', '')    #邮箱的账户 ,密码
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()



if __name__ == '__main__':

    me='741494582@qq.com'
    urls=[url_qhd,url_cz,url_xi_an]       #地点集合
    address = []                          #收件人
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