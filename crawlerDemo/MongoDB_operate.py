'''
>>目标：
将mongoDB中Taoey数据库下的Ali_farmer表中的文章以utf-8编码形式存成TXT文本，TXT文本只需要文章标题和文章文字内容。
TXT标题即为文章标题（对于标题中不能处理的特殊符号直接去除掉）
>>技术问题
1.去除文件名中的特殊字符（正则方法）
2.学习查询mongoDB中的数据 推荐博客：http://www.cnblogs.com/jayruan/p/5123613.html
3.文件流的写入
4.文章写入时的编码问题
>>其他
python version :3.5.1
author :黄为涛
数据库数据为该项目下Data下的MongoDB_operate_data.json
'''
from pymongo import MongoClient
import re
import codecs
# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title

client=MongoClient()
db=client.Taoey
p=db.Ali_farmer.find({},{'文章标题':1,'文章内容':1})

for i in p:
    title=validateTitle(i['文章标题'])
    f=codecs.open('D:/temp/{}.txt'.format(title),'a','utf-8')
    f.write(i['文章内容'])
    f.close()