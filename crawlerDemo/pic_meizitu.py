'''
1.修改了上个版本的爬取遇到无效图片停止的bug
2.有了更好的交互界面
3.增加了本地文档的判断，避免断线之后的重新爬取


下个版本目标：
1.实现多线程图片
2.断线（异常）重新启动爬虫后，从断线处重新开始

'''


from bs4 import BeautifulSoup
import requests
import re,os
import threading
import urllib,urllib.request


url=['http://www.meizitu.com/a/xinggan_2_{}.html'.format(str(i)) for i in range(1,12)]

album_url=[]
#主题下的所有小标题
def get_pics_urls(url):
    global album_url
    header={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
    req=requests.get(url,header)
    req.encoding='gb2312'
    soup=BeautifulSoup(req.text,'lxml')
    p=soup.select('div.pic > a ')
    #soup2=BeautifulSoup(str(p),'lxml')
    #result=soup2.find_all('a',attrs={'target':True,'href':re.compile(r"http://www.meizitu.com/a(\s\w+)?")})
    #types=soup.find_all('a',attrs={'href':re.compile(r"http://www.meizitu.com/a(\s\w+)?"),'title':True})
    #print(result)
    for i in p:
        album_url.append(dict(i.attrs)['href'])

#获得图片
def get_all_pictures(url):
    Header = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
    }
    req = requests.get(url, Header)
    req.encoding = 'gb2312'
    soup = BeautifulSoup(req.text, 'lxml')
    p=soup.select('div#picture > p > img')
    albumNames = soup.select('div.metaRight > h2 > a')
    albumName=albumNames[0].get_text()
    for i in p:
        pic_url=dict(i.attrs)['src']
        cdir=os.getcwd()
        path=cdir+'\\'+albumName
        #print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        pathfile = path + '\\' + pic_url[-6:]

        if os.path.exists(pathfile):
            print(pathfile+'图片已存在')
        else:
            # ........................................
            requ = urllib.request.Request(pic_url, headers=Header)
            try:
                imgData = urllib.request.urlopen(requ).read()
                with open(pathfile, 'wb') as f:
                    f.write(imgData)
                    f.close()
                print(pathfile)
            except:
                print('write error' + pathfile)
            # ..........................................




for i in url:
    print(i)
    get_pics_urls(i)
    print(album_url)

for j in album_url:
    print(j)
    get_all_pictures(j)


#http://www.meizitu.com/a/4742.html   有问题的连接  debug测试
#get_all_pictures('http://www.meizitu.com/a/4742.html')

