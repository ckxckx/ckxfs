# -*- coding: utf-8 -*-
from datetime import datetime
import pymongo
import scrapy
from wooyun.items import WooyunItem
from scrapy.conf import settings
import random
#
#
# + 运行scrapy crawl freebuf -a page_max=1  -a local_store=false -a update=false，有三个参数用于控制爬取：
#
#     -a page_max: 控制爬取的页数，默认为1，如果值为0，表示所有页面
#
#     -a local_store: 控制是否将每个漏洞离线存放到本地，默认为false
#
#     -a update：控制是否重复爬取，默认为false


#http://www.freebuf.com/vuls/page/3

ALLOWURL='http://www.freebuf.com'
STARTS_URL='http://www.freebuf.com/vuls/'
PAGE="vuls/page/%d"       ##抽取目录
XPATH1='//dl/dt/a/@href'  ##抽取目录中的url
XPATH2='//title/text()'   ##抽取标题
XPATH3='//span[@class="name"]/a/text()'
AUTHOR='EVIL_CALVIN'  ##操作人名称
SAVEPIC=False   ##判断是否存储图片
SPIDERNAME="freebuf"  ###爬虫名称
PAGE_MAX=1    ##抓取页数


class WooyunSpider(scrapy.Spider):
    name = SPIDERNAME          #####传入参数的位置1
    # allowed_domains = ["freebuf.com"]         #####传入参数的位置1
    start_urls = [
        STARTS_URL  #####传入参数的位置1
    ]

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],local_store=settings['LOCAL_STORE_DEFAULT'],\
            update=settings['UPDATE_DEFAULT'],*args, **kwargs):
        # self.page_max = int(page_max)
        self.page_max = PAGE_MAX          ####传入参数控制爬取页数

        self.local_store = 'true' == local_store.lower()
        self.update = 'true' == update.lower()

        self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.total_count_bugs = self.collection.find().count()


    def closed(self,reason):
        self.client.close()

    def parse(self, response):
        if self.page_max == 0:
            pass
        else:
            end_page = self.page_max

        for n in range(1,end_page + 1):
            page = PAGE %n    ######传入参数位置2
            url = response.urljoin(page)
            yield scrapy.Request(url, self.parse_list)

    def parse_list(self,response):
        links = response.xpath(XPATH1).extract()   ####传入参数位置3，规则提取url的规则
        for url in links:
            print url
            yield scrapy.Request(url, self.parse_detail)

    def parse_detail(self,response):
        item = WooyunItem()
        item['title'] = response.xpath(XPATH2).extract()[0].split("|")[0]
        #####暂且id按照简单的1234......
        self.total_count_bugs=self.total_count_bugs+1
        item['wooyun_id']=str(self.total_count_bugs)
        item['uploader'] = response.xpath(XPATH3).extract()[0].split("|")[0]
        item['author'] =AUTHOR  ####可有可无的传入参数点4
        item['html'] = response.body.decode('utf-8','ignore')
        item['datetime'] = datetime.now()
        item['image_urls']=[]

        ##是否存储图片到本地
        self.local_store = SAVEPIC
        if self.local_store:
            image_urls = response.xpath('//img/@src').extract()
            for u in image_urls:
                if self.__check_ingnored_image(u):
                    continue
                if u.startswith('/'):
                    u = ALLOWURL + u
                item['image_urls'].append(u)
        return item

    def __check_ingnored_image(self,image_url):
        for ignored_url in settings['IMAGE_DOWLOAD_IGNORED']:
            if ignored_url in image_url:
                return True

        return False

