"""
轻小说文库简单爬虫
"""
from selenium import webdriver
from lxml import etree
import time
import os,codecs

domian="http://www.wenku8.com/novel/2/2272/index.htm"



urls_xpath="//td[@class='ccss']/a/@href"   #每篇文章的地址
name_xpath="//*[@id='title']"              #作品名
author_xpath="//*[@id='info']"              #作者名
title_xpath="//*[@id='title']/text()"      #章节名
con_xpath="//*[@id='content']"             #内容


driver=webdriver.PhantomJS()
urls=[]
NAME=""
AUTHOR=""
domian2=domian.replace("index.htm","")

def getInfo():
    '获取作品名，作者等内容'
    global NAME,AUTHOR
    driver.get(domian)
    selector=etree.HTML(driver.page_source)
    name=selector.xpath(name_xpath)
    author=selector.xpath(author_xpath)
    driver.close

    for i in name:
        NAME=i
    for i in author:
        AUTHOR=i


if __name__ == '__main__':
    getInfo()
