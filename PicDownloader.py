import threading
import time
import urllib
import urllib.request
import os,queue,re
from bs4 import BeautifulSoup

def getUrl(name,hostUrls,girlsUrls,flag):
    while  not flag.isSet():
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        try:
            hostUrl=hostUrls.get(timeout=2)
        except queue.Empty:
            print("queue empty")
            return
        request=urllib.request.Request(hostUrl,headers=headers)
        response=urllib.request.urlopen(request)
        data=response.read().decode('gbk')
        soup=BeautifulSoup(data)
        tag_lady=soup.find_all("a",attrs={"class":"lady-avatar"})
        for tag_href in tag_lady:
            girlsUrls.put("https:"+tag_href['href'])
            print("录入：https:"+tag_href['href'])
        hostUrls.task_done()
        print("getUrl is working")

def getImg(name,girlsUrls,flag):
    while not flag.isSet():
        user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'
        headers={'User-Agent':user_agent}
        try:
            ur=girlsUrls.get(timeout=5)
        except queue.Empty:
            print(name+" imgqueue empty")
            return
        pattern=re.compile(r"/(\d+).htm")
        items=pattern.findall(ur)
        girlUrl="https://mm.taobao.com/self/aiShow.htm?userId="+items[0]
        request=urllib.request.Request(girlUrl,headers=headers)
        response=urllib.request.urlopen(request)
        data=response.read()
        soup=BeautifulSoup(data)
        fileName=soup.head.title.contents
        fileName[0]=fileName[0].rstrip()
        tag_div=soup.find('div',attrs={"class":"mm-aixiu-content"})
        imgs=tag_div.find_all("img",attrs={})
        if len(imgs)==0:
            girlsUrls.task_done()
            return
        path=cdir+'/'+str(fileName[0])
        if not os.path.exists(path):
            os.makedirs(path)
        n=0
        for img in imgs:
            n=n+1
            link=img.get('src')
            if link:
                s="http:"+str(link)
                i=link[link.rfind('.'):]
                try:
                    request=urllib.request.Request(s)
                    response=urllib.request.urlopen(request)
                    imgData=response.read()
                    pathfile=path+r'/'+str(n)+i
                    with open(pathfile,'wb') as f:
                        f.write(imgData)
                        f.close()
                        print("thread "+name+" write:"+pathfile)
                except:
                    print(str(name)+" thread write false:"+s)
        girlsUrls.task_done()

#start=time.time()
if __name__=='__main__':
    start=time.time()
    hostUrls=queue.Queue()
    girlsUrls=queue.Queue()
    cdir=os.getcwd()
    url='https://mm.taobao.com/json/request_top_list.htm?page='
    flag_girl=threading.Event()
    flag_img=threading.Event()
    for i in range(1,3):
        u=url+str(i)
        hostUrls.put(u)
    threads_girl = threading.Thread(target=getUrl, args=(str(1), hostUrls,girlsUrls,flag_girl))
    threads_img = [threading.Thread(target=getImg, args=(str(i+1), girlsUrls,flag_img))
               for i in range(8)]
    threads_girl.start()
    while(girlsUrls.empty()):
        print("wait..")
        time.sleep(0.1)
    for t in threads_img:
        t.start()
    hostUrls.join()
    flag_girl.set()
    girlsUrls.join()
    flag_img.set()
    for t in threads_img:
        t.join()
    end=time.time()
    print("run time:"+str(end-start))