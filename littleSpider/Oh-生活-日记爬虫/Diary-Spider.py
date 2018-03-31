import requests


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

def getDiaryIdDics(month):
    '''
    获取每月的日记id号列表
    :param month:
    :return:
    '''
    url = "https://ohshenghuo.com/api/diary/simple_by_month/2018/3/"
    web = requests.get(url=url,headers=getHeaders())
    diariesJson = web.json()
    pass

def saveDiary(date,id):
    '''
    保存一条日记到本地，存储方式为.md 文件格式
    :return:
    '''
    diaryUrl = "https://ohshenghuo.com/api/diary/{}".format(id)
    diaryJson = requests.get(url=diaryUrl,headers=getHeaders()).json()
    print(diaryJson)

    for i in diariesJson['diaries'].items():
        # i为一个元组 i[0]为日期，用于本地数据的文件名;i[1]为日记id，用于提取日记内容
        saveDiary(i[0],i[1])
        pass
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

    getMonthList()
    pass



