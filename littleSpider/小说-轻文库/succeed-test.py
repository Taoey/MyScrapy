"""
轻小说文库简单爬虫
"""
from selenium import webdriver
from lxml import etree
import time
import os,codecs
#http://www.wenku8.com/novel/1/1143/index.htm
tempStr = input("请输入作品地址：")
DOMAIN = tempStr.replace(" ", "")

urls_xpath="//td[@class='ccss']/a/@href"   #每篇文章的地址
name_xpath="//*[@id='title']/text()"              #作品名
author_xpath="//*[@id='info']/text()"              #作者名
title_xpath="//*[@id='title']/text()"      #章节名
con_xpath="//*[@id='content']"             #内容

driver=webdriver.Firefox()
urls=[]
NAME=""
AUTHOR=""
DOMAIN2=DOMAIN.replace("index.htm","")

def getInfo():
    '获取作品名，作者等内容'
    global NAME,AUTHOR
    driver.get(DOMAIN)
    selector=etree.HTML(driver.page_source)
    name=selector.xpath(name_xpath)
    author=selector.xpath(author_xpath)
    driver.close

    for i in name:
        NAME=i
    for i in author:
        AUTHOR=i

def getUrls():
    '获取每个章节的url'
    driver.get(DOMAIN)
    selector=etree.HTML(driver.page_source)
    urlCon=selector.xpath(urls_xpath)
    driver.close
    for i in urlCon:
        urls.append(DOMAIN2+i)

def writeCon(con):
    '写入内容'
    cdir = os.getcwd()
    filepath=cdir+"\\{}-{}.txt".format(NAME,AUTHOR)
    f=codecs.open(filepath,"a","utf-8")
    f.write(con)
    pass

def download(url):
    '下载每章内容'
    try:
        driver.get(url)
        selector=etree.HTML(driver.page_source)
        title=selector.xpath(title_xpath)
        con=selector.xpath(con_xpath)
        driver.close

        for i in title:
            writeCon(i)
            print("正在下载：‘{}’......".format(i))
        for i in con:
            writeCon("".join(i.xpath('descendant-or-self::text()')).replace("本文来自 轻小说文库(http://www.wenku8.com)","").replace("最新最全的日本动漫轻小说 轻小说文库(http://www.wenku8.com) 为你一网打尽！",""))
            print("-----------")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    getInfo()
    getUrls()
    for url in urls:
        download(url)
        time.sleep(4)

    print("本书下载完成")
