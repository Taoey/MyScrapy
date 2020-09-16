from selenium import webdriver
from lxml import etree
from MyBrowser import Browser
import Main

def test_desc():
    url = "https://www.juzimi.com/jianjiejieshao/1051"
    driver = webdriver.Firefox()
    driver.get(url)
    selector = etree.HTML(driver.page_source)
    descs_element = selector.xpath("//*[@class='jianjiecontext']/br")
    for element in descs_element:
        print(element.text)
        print(element.tail) # 解决br标签问题
    driver.close()
    pass

def test_Mydrive():
    url = "https://www.baidu.com/"
    data = Browser.get_data(url)
    print(data)

def test_get_book_list():
    url = "https://www.juzimi.com/jingdian/zuopin/602"
    book_list = Main.get_book_list(url)
    print(book_list)

def test_get_book_data():
    url = "https://www.juzimi.com/article/%E7%BA%A2%E7%8E%AB%E7%91%B0%E4%B8%8E%E7%99%BD%E7%8E%AB%E7%91%B0"
    Main.get_book_data(url)

def test_sentence():
    url = "https://www.juzimi.com/article/%E7%BA%A2%E7%8E%AB%E7%91%B0%E4%B8%8E%E7%99%BD%E7%8E%AB%E7%91%B0"
    page_source = Browser.get_data(url).replace("<br/>", "")
    sentence_selector = etree.HTML(page_source)
    sentence_elements = sentence_selector.xpath("//*[@class='xlistju']")
    for e in sentence_elements:
        print(e.text)

def test_string():
    str = "<br/>"
    str = str.replace("<br/>","")
    print(str)


def test_json():
    data = {}
    data.update({"name":"tao"})
    print(data)
if __name__ == '__main__':
    pass