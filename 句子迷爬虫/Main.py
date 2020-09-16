import random
import time

from MyBrowser import Browser
from lxml import etree
from pymongo import MongoClient
import logging

def mydb():
    client = MongoClient()
    return client.ju_friends



def get_book_list(url,page):
    bookurl_list = []

    page_source = Browser.get_data(url)
    selector = etree.HTML(page_source)
    # 获取图书页数
    book_pages = selector.xpath("//*[@class='pager-item']")
    page_num = len(book_pages)
    if page_num ==0:
        page_num=1
    print('页数：{}'.format(page_num+1))
    book_page_urls = [url+"?page={}".format(i) for i in range(page-1,page_num)]

    for url in book_page_urls:
        page_source = Browser.get_data(url)
        selector = etree.HTML(page_source)
        book_name_elements = selector.xpath("//*[@class='xqallarticletilelink']")
        # 获取URL
        for element in book_name_elements:
            url = "https://www.juzimi.com" + element.get("href")
            bookurl_list.append(url)
        time.sleep(random.randint(3,6))
    print("图书数量：{}".format(len(bookurl_list)))
    print(bookurl_list)
    return  bookurl_list


def get_book_data(url):

    try:
        page_source = Browser.get_data(url)
    except:
        print("网络异常")
    selector = etree.HTML(page_source)

    # 获取简介+url
    desc_element = selector.xpath("//a[@class='wridescjiajie']")[0]
    name = desc_element.text.replace("简介","").replace("《","").replace("》","")
    desc_url = "https://www.juzimi.com"+desc_element.get("href")

    # 进入简介页面
    desc_page_source = Browser.get_data(desc_url)
    desc_selector = etree.HTML(desc_page_source)

    author = desc_selector.xpath("//*[@class='xqjianjieagewr']/a")[0].text
    img_url = "https:" + desc_selector.xpath("//*[@class='jianjieconpichtml']/img")[0].get("src")

    # 简介中含有br标签，需要处理
    desc = desc_selector.xpath("//*[@class='jianjiecontext']")[0].text
    try:
        descs_element = desc_selector.xpath("//*[@class='jianjiecontext']/br")
        for element in descs_element:
            desc += "\n" + element.tail
    except:
        pass
    print("作者：{}".format(author))
    print("图片url：{}".format(img_url))
    print("简介url：{}".format(desc_url))
    print("简介：{}".format(desc))

    # 获取图书页数
    page_num = 1
    try:
        page_num = selector.xpath("//*[@class='pager-last']/a")[0].text
    except:
        page_num = len(selector.xpath("//*[@class='pager-item']"))
        if page_num == 0:
            page_num =1

    print("句子页数为：{}".format(page_num))

    #爬取句子
    sentence_list =[]
    sentence_urls = [url+"?page={}".format(i) for i in range(int(page_num))]
    page_count = 0
    for sentence_url in sentence_urls:
        print("共{}页，正在爬取第{}页，还剩{}页".format(page_num,page_count,int(page_num)-page_count))
        page_count +=1
        try:
            page_source = Browser.get_data(sentence_url).replace("<br/>","")
        except:
            print("网络异常")
        sentence_selector = etree.HTML(page_source)
        sentence_elements = sentence_selector.xpath("//*[@class='xlistju']")

        for e in sentence_elements:
            sentence_list.append(e.text)
            print(e.text)
        time.sleep(random.randint(3,10))
    print(sentence_list)
    print("共爬取{}条句子".format(len(sentence_list)))

    # 保存数据
    data = {
        'name': name,
        "url": url,
        "author": author,
        "desc_url": desc_url,
        "desc": desc,
        "pic_url": img_url,
        "pages": page_num,
        "sentence": sentence_list,
    }
    mydb().book.insert_one(data)
    print("保存数据成功")


if __name__ == '__main__':
    url = "https://www.juzimi.com/jingdian/zuopin/769"
    urls = [
        "https://www.juzimi.com/jingdian/zuopin/1178"
    ]
    for url in urls:
        book_list = get_book_list(url,1)
        index = 0
        for book_url in book_list:
            get_book_data(book_url)
            time.sleep( random.randint(6,10))
            print("还剩{}本".format(len(book_list)-index-1))
            index = index +1




