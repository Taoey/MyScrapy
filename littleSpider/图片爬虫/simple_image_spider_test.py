import urllib.request
import os


def test_img_spider_1():
    """
    利用的是urllib.request 这个库 直接使用urlopen获取url数据之后使用read方法读出数据，
    再将数据保存在本地
    :return:
    """
    cdir = os.getcwd()
    path = cdir+"\\"+"pic.jpg"

    url = 'http://www.pptbz.com/pptpic/UploadFiles_6909/201203/2012031220134655.jpg'
    imgData = urllib.request.urlopen(url).read()
    with open(path, 'wb') as f:
        f.write(imgData)
        f.close()

def test_img_spider_2():
    """
    这个爬虫主要利用的是urlretrieve这个方法，比较简单，一句话就能搞定
    :return:
    """
    cdir = os.getcwd()
    path = cdir+"\\"+"pic.jpg"
    url = 'http://www.pptbz.com/pptpic/UploadFiles_6909/201203/2012031220134655.jpg'

    urllib.request.urlretrieve(url, path)
