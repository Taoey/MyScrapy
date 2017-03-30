from spy80s.items import Spy80SItem
from scrapy.spider import Request
import scrapy


class Spider_80s(scrapy.Spider):
    name='spider_80s'
    start_urls=[
        'http://www.80s.tw/movie/list',
    ]

    def start_requests(self):
        for i in range(1, 5):
            url = "http://www.80s.tw/movie/list/-----p" + str(i)
            yield Request(url=url, callback=self.parse)

    def parse(self,response):
        item_title=response.xpath("//*[@class='h3']/a/text()").extract()
        item_score=response.xpath("//*[@class='poster_score']/text()").extract()
        for i in range(0,len(item_title)):
            item=Spy80SItem()
            item['_name']=''.join(item_title[i].replace('\n','').replace(' ',''))
            item['_score']=''.join(item_score[i])
            # print(item)
            yield item



