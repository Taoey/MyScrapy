from selenium import webdriver
from lxml import etree

urls=["http://www.juzimi.com/writer/29766?page={}".format(i) for i in range(23)]
driver = webdriver.Firefox()

COUNT=0

def getResult(url):
    global COUNT
    try:
        driver.get(url)
        selector=etree.HTML(driver.page_source)
        result=selector.xpath("//*[@class='xlistju']")
        driver.close

        for i in result:
            print(str(COUNT)+"."+"".join(i.xpath('descendant-or-self::text()')).replace("\n","").replace(" ",""))
            print("\n")
            COUNT=COUNT+1
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for url in urls:
        getResult(url)
