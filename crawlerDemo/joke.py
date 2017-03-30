# coding=utf-8
from bs4 import BeautifulSoup
import requests
import codecs
import time
ID=0
'''
author      : 黄为涛
version     ：Python3
codeVersion ：1.0
'''
def getHappy(url):
    global ID
    time.sleep(0)
    webData = requests.get(url)
    soup = BeautifulSoup(webData.text, 'lxml')

    names = soup.select('div.author.clearfix > a > h2 ')
    contents = soup.select('div.content > span ')
    votes = soup.select('span.stats-vote > i ')
    comments = soup.select('a[class="qiushi_comments"] > i')

    f = codecs.open('D:/temp.txt', 'a','utf-8')#编码格式的注
    for name, content, vote, comment in zip(names, contents, votes, comments):
        data = {
            'name': name.get_text(),
            'content': content.get_text(),
            # 'vote'       :  vote.get_text(),
            # 'commentNum' :  comment.get_text(),
        }
        ID += 1
        f.write(u'{}{}{}{}{}{}{}'.format('★', str(ID), '★', data['name'], '\n', data['content'], '\n\n'))#注意文件的读取格式方式
        print('download joke{}'.format(str(ID)))
    f.close()


# main
urls=['http://www.qiushibaike.com/text/page/{}/?s=4962348'.format(str(i)) for i in range (1,36)]
print('爬取时间较长请稍等.......')
time.sleep(2)
for url in urls:
    getHappy(url)
print('下载已完成,本笑话集保存在：D:/temp.txt')