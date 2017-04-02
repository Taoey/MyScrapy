# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spy80s.items import Spy80SItem
from scrapy.conf import settings
import pymongo

class Spy80SPipeline(object):

    def __init__(self):
        # client = MongoClient()
        # db = client.Taoey
        host=settings['MONGDB_HOST']
        port=settings['MONGO_PORT']
        dbName=settings['MONGODB_DBNAME']
        client=pymongo.MongoClient(host=host,port=port)
        tdb=client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        print('连接成功了')

    def process_item(self, item, spider):
        self.post.insert(dict(item))
        return item
