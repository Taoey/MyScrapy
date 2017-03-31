'''
使用了selenium简单爬取京东的服装数据

缺点：
1.没有使用多线程
2.没有错误处理机制
3.应该加入异常重爬机制


'''
import os,time
from lxml import etree
from selenium import webdriver
from pymongo import MongoClient


class items:

    def __init__(self,title="",commit="",price="",store="",self_sell=""):
        self.title=title
        self.commit=commit
        self.price=price
        self.store=store
        self.self_sell=self_sell

def getData(src_code):
    "获得商品对象数据，返回一个list"
    itemsList=[]
    selector = etree.HTML(src_code)
    prices = selector.xpath(
        "//*[@id='J_goodsList']/ul//li[@class='gl-item']//div[@class='p-price']/strong/i/text()")
    commits = selector.xpath("//*[@id='J_goodsList']/ul//li[@class='gl-item']//div[@class='p-commit']/strong/a/text()")
    stores= selector.xpath("//*[@id='J_goodsList']/ul//li[@class='gl-item']//div[@class='p-shop']")
    titles = selector.xpath(
        "//*[@id='J_goodsList']/ul//li[@class='gl-item']//div[@class='p-name p-name-type-2']/a/em")
    icons = selector.xpath("//*[@id='J_goodsList']/ul//li[@class='gl-item']//div[@class='p-icons']")
    # print(len(prices),len(commits),len(stores),len(titles),len(icons))
    for i in range(0,len(prices)):
        temp_item=items()
        temp_item.title=titles[i].xpath('string(.)').strip()
        temp_item.commit=commits[i]
        temp_item.store=stores[i]
        temp_item.price=prices[i]
        if etree.tostring(stores[i]).find(b"span")==-1:
            temp_item.store=""
        else:
            temp_item.store=stores[i].xpath("string(.)").strip()


        if etree.tostring(icons[i]).find(b"img")==-1:
            temp_item.self_sell="False"
        else:
            temp_item.self_sell="True"
        itemsList.append(temp_item)
    return itemsList

def down_page():
    "控制浏览器向下滚动到底"
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(5)

def insert_data(data_list):
    "将数据插入到数据库"
    for j in data_list:
        data={
            "商品标题":j.title,
            "商品价格":j.price,
            "评论数量":j.commit,
            "所售商店":j.store,
            "是否自营":j.self_sell,
        }
        db.jingdong_clothing.insert_one(data)



#main
url_1='https://search.jd.com/Search?keyword=%E6%9C%8D%E8%A3%' \
     '85&enc=utf-8&wq=%E6%9C%8D%E8%A3%85&pvid=12da848282864849ae3ceda2666c8b72'
url_2='https://search.jd.com/Search?keyword=%E6%9C%8D%E8%A3%85%E4%BA%AC%E4%B8%9C%E8%87%AA%E8%90%A5&enc=utf-8&w' \
     'q=%E6%9C%8D%E8%A3%85%E4%BA%AC%E4%B8%9C%E8%87%AA%E8%90%A5&pvid=79463552e98d4812ae84a850009efbb0'
start_url=[url_1,url_2]

chromedriver = "D:\CCApplication\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox()

client = MongoClient()
db = client.Taoey

for i in start_url:
    print("url：{}\n数据开始获取".format(i))
    driver.get(i)
    down_page()
    dataList = getData(driver.page_source)
    insert_data(dataList)
    #selenium方法获取标签文本内容
    page_num=int(driver.find_element_by_xpath("//*[@id='J_bottomPage']/span[2]/em[1]/b").text)
    for k in range(0,page_num-1):
        driver.find_element_by_xpath("//a[@class='pn-next']").click()
        down_page()
        dataList = getData(driver.page_source)
        insert_data(dataList)
        print("page{}数据获取完毕".format(k))
    print("url：{}\n数据获取完毕".format(i))








