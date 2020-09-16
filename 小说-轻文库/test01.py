from selenium import webdriver
from lxml import etree

domian="http://www.wenku8.com/novel/1/1213/"
start=37500
end=9782

title_xpath="//*[@id='title']/text()"
con_xpath="//*[@id='content']"


driver=webdriver.PhantomJS()
urls=[domian+"{}.htm".format(i) for i in range(start,end)]

def download(url):
    try:
        driver.get(url)
        selector=etree.HTML(driver.page_source)
        title=selector.xpath(title_xpath)
        con=selector.xpath(con_xpath)
        driver.close

        for i in title:
          print(i)
        for i in con:
            print("".join(i.xpath('descendant-or-self::text()')).replace("本文来自 轻小说文库(http://www.wenku8.com)","").replace("最新最全的日本动漫轻小说 轻小说文库(http://www.wenku8.com) 为你一网打尽！",""))

    except Exception as e:
        print(e)
if __name__ == '__main__':
    for url in urls:
        download(url)