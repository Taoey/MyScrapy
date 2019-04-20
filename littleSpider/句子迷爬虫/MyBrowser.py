import requests
from selenium import webdriver

class Browser:
    def __init__(self):
        print("Mydriver初始化完成")
        self.driver = webdriver.Firefox()

    @staticmethod
    def get_data(url):
        driver = webdriver.Firefox()
        driver.get(url)
        result = driver.page_source
        driver.close()
        return result
        # header = {
        #         'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        #     }
        # req = requests.get(url, header)
        # req.encoding = 'utf-8'
        # return req.text

    def get_data_use_brower(self,url):
        driver = webdriver.Firefox()
        driver.get(url)
        result = driver.page_source
        driver.close()
        return result