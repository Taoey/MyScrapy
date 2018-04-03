import requests

def getHeaders():
    '''
    从headers文件 中提取headers
    :return:
    '''
    f = open(r'headers', 'r')
    headers = {}
    for line in f.read().split('\n'):
        name ,value = line.strip().split(':',1)
        headers[name]=value
    f.close()
    return headers

def getData():
    f = open('data','r')
    data = {}
    for line in f.read().split('\n'):
        name,value = line.split('\t',1)
        data[name] = value
    f.close()
    return data

if __name__ == '__main__':

    url = 'https://i.cnblogs.com/BlogBackup.aspx'
    web = requests.post(url,headers=getHeaders(),data=getData())
    web.encoding = 'utf-8'
    print(web.text)
