# -*- coding: utf-8 -*-
BOT_NAME = 'spy80s'
SPIDER_MODULES = ['spy80s.spiders']
NEWSPIDER_MODULE = 'spy80s.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
ROBOTSTXT_OBEY = True

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

ITEM_PIPELINES = {
    'spy80s.pipelines.Spy80SPipeline':300
}

MONGODB_HOST = '127.0.0.1'
MONGODB_POST = 27017
MONGODB_DBNAME = 'Taoey'
MONGODB_DOCNAME = '_80s_movies'


