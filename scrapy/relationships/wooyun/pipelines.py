# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime
import copy
import json
import codecs
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
########并没有对图片管道进行重写，如果

        ######看来这个images是内置于item的列表集合，这个里面的信息蛮重要的
        # for img in item['images']:




class MongoDBPipeline(object):
    def __init__(self):
        self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.log = logging.getLogger(spider.name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        post_data = copy.deepcopy(item)
        self.collection.insert_one(dict(post_data))

        return item

class WooyunSaveToLocalPipeline(object):
    def process_item(self,item,spider):
        pass
        return item

    def __process_html(self,item):
        pass
        return True
