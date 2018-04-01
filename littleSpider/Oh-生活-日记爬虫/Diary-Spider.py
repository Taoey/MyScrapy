import requests
import os

def getHeaders():
    '''
    从headers.txt 中提取headers
    :return:
    '''
    f = open(r'headers.txt', 'r')
    headers = {}
    for line in f.read().split('\n'):
        name ,value = line.strip().split(':',1)
        headers[name]=value
    f.close()
    return headers

def getMonthList():
    '''
    获取要提取的年月份字典合集
    :return: monthList = ['2018/2','2018/3']
    status :done
    '''
    monthList = []
    start = "2017/8"
    end = "2019/1"
    startYear,startMonth = start.split('/')
    endYear,endMonth = end.split('/')
    startYear = int(startYear)
    startMonth = int(startMonth)
    endYear = int(endYear)
    endMonth = int(endMonth)

    currentYear = startYear
    currentMonth = startMonth

    MonthNum = (endYear-startYear)*12+endMonth-startMonth+1
    count = 0
    while count < MonthNum:
        monthList.append("%d/%d" % (currentYear,currentMonth))
        currentMonth+=1
        if currentMonth ==13:
            currentMonth = 1
            currentYear+=1
        count+=1
    return monthList

def getDiaryIdDics(date):
    '''
    获取每月的日记id号列表
    :param month:
    :return:
    '''
    url = "https://ohshenghuo.com/api/diary/simple_by_month/{}/".format(date)
    web = requests.get(url=url,headers=getHeaders())
    diariesJson = web.json()["diaries"]
    return diariesJson

def saveDiary(dir,date,id):
    '''
    保存一条日记到本地,文件格式应可选(未完成)
    :return:
    '''
    diaryUrl = "https://ohshenghuo.com/api/diary/{}".format(id)
    diaryJson = requests.get(url=diaryUrl,headers=getHeaders()).json()

    weather = diaryJson['diary']['weather']
    mood = diaryJson['diary']['mood']
    weekday = diaryJson['diary']['weekday']
    content = diaryJson['diary']['content']
    fileName = "%s_%s_%s_%s" % (date,weekday,weather,mood)
    f = open(dir+os.sep+fileName,"w")
    f.write(content)
    f.close()
    pass

def saveDiaryAsJson(id):
    '''
    保存一条日记的全部数据为json文件
    :param id:
    :return:
    '''



if __name__ == '__main__':
    # startDate = input("Please Input Strat Date(Like 2018/3):")
    # endDate = input("Please Input End Date(Like 2018/4):")

    startDate = '2018/3'
    endDate = '2018/3'

    print("pleas wait a moment ,loading.......")
    monthList = getMonthList()
    diarys = {}
    #合并字典
    for date in monthList:
        diarys = dict(diarys,**getDiaryIdDics(date))
    #建立文件夹
    dir = 'diarys'
    if not os.path.exists(dir):
        os.mkdir(dir)

    for date in diarys.items():
        print("saving %s ..." % (date[0]))
        saveDiary(dir,date[0],date[1])
        print('%s done' %(date[0]))



