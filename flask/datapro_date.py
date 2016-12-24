# -*- coding: utf-8 -*-
import time
import pymongo;
from operator import itemgetter

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB_ckx = 'ckxlogin'
MONGODB_DB = 'wooyun'
MONGOTABLE = 'loginlist'
connection_string = "mongodb://%s:%d" % (MONGODB_SERVER, MONGODB_PORT)
MONGODB_COLLECTION_BUGS = 'wooyun_list'
MONGODB_COLLECTION_DROPS = 'wooyun_drops'
ROWS_PER_PAGE = 20



client = pymongo.MongoClient(connection_string)
db = client['wooyun']
weichuli = db['relationships']
chulilist=db['chulilist']
item={}
llu=weichuli.find()
for lu in llu:
    for it in lu['leixing']:
        item['leixing']=it
        item['date']=lu['riqi']
        db['riqi_leixing_guanlian'].insert(item)
        item={}


