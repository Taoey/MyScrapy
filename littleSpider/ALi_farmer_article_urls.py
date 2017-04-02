#conding=utf-8
from bs4 import BeautifulSoup
import requests
'''
说明：
获取所有特定标签的属性，先用一个BeautifulSoup对象获取所有的特定标签列表，
然后再用一个BeautifulSoup对象解析上一个列表String最后用类似   标签名['属性'] 来获取对应的属性
注意：要用一个for循环来遍历，否者只会获得一个数据
'''
'''
实例：获取阿里研究院涉农标签的所有文章的URL
author ：黄为涛
python version：3.5.1
'''
page_url=['http://www.aliresearch.com/blog/article/lists/category/47/page/{}.html'.format(str(i)) for i in range(1,67)]
header={
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
}
for page in page_url:
    req=requests.get(page,header)
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'lxml')
    urls=soup.select('h3.text-more.media-heading > a')
    soup2=BeautifulSoup(str(urls),'lxml')
    for i in soup2.select('a'):
        url_really='http://www.aliresearch.com/'+i['href']
        print(url_really)