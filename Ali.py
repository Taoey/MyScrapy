from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
'''
>>目标
将阿里研究院（http://www.aliresearch.com/）里面关于农村、县域的文章，
使用python爬取下来；并将爬取下来的文章存入MongoDB数据库
>>说明：
本例需要安装MongoDB数据库，函数getData()是该将文本写入数据库中
>>技术点：
1.字符串的截取处理
2.利用pymongo操作数据库
3.代码优化，利用函数
>>其他
Python version: 3.5.1
author : 黄为涛
下一步：争取实现多线程，和 scrapy框架实现
'''
def getMarks(str,remarks):
    left=remarks.find(str)
    right=remarks.find('\n',left)
    s=remarks[left+3:right]
    return s;

def getData(url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
    req = requests.get(url, header)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'lxml')

    titles = soup.select('div.common_block_title.clearfix > h2')
    title = titles[0].get_text()
    remarks = soup.select('span.pull-left')
    remark=remarks[0].get_text()
    cons = soup.select('section[id="contents"]')
    con = cons[0].get_text()

    src = getMarks('来源',remark)
    type = getMarks('分类',remark)
    time = getMarks('时间',remark)
    numIndex = getMarks('阅读',remark).find('次')
    readNum = getMarks('阅读',remark)[0:numIndex]

    # 数据库存储数据
    client = MongoClient()
    db = client.Taoey
    db.Ali_farmer.insert_one(
        {
            '文章标题': title,
            '来源': src,
            '分类': type,
            '时间': time,
            '阅读': readNum,
            '文章内容': con
        }

    )
urls = []
def getURList(page_url):
    global urls
    '''
    一定要注意函数中的变量不要和外边重复，否则会导致一些意想不到的问题（开始bug：‘urls’变量命名重复，导致一些url获取不到）
    '''
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
    for page in page_url:
        req=requests.get(page,header)
        req.encoding='utf-8'
        soup=BeautifulSoup(req.text,'lxml')
        urlss=soup.select('h3.text-more.media-heading > a')
        soup2=BeautifulSoup(str(urlss),'lxml')
        for i in soup2.select('a'):
            url_really='http://www.aliresearch.com/'+i['href']
            urls.append(url_really)


page_url=['http://www.aliresearch.com/blog/index/search/keywords/%E5%8E%BF%E5%9F%9F/page/{}.html'.format(str(i)) for i in range(1,14)]
page_url2=['http://www.aliresearch.com/blog/index/search/keywords/%E5%86%9C%E6%9D%91/page/{}.html'.format(str(i)) for i in range(1,14)]
getURList(page_url)
getURList(page_url2)
count=0
for i in urls:
    getData(i)
    count=count+1
    print('第{}篇文章下载完毕'.format(str(count)))