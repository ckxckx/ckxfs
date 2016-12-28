# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#这段代码则1对多——上传者对应的文章、文章类型、人气指数等等存储到设计的表格中

import pymongo;
from bson.objectid import ObjectId

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
chuliname=db['uploader_aim']
mubiao=db['leixing_aim']
chuli=db['chulilist']
biao=chuli.find_one()
mydict={}

for i in biao['leixing']:
    mydict={}
    rongqi1=[]
    rongqi2=[]
    cc=weichuli.find({"leixing":i})
    for c in cc:
        rongqi1.append(c["title"])
        rongqi2.append(c["uploader"])
    # rongqi1=list(set(rongqi1))
    # rongqi2=list(set(rongqi2))
    mydict["leixing"]=i
    mydict["titles"]=rongqi1
    mydict["uploaders"]=rongqi2
    mubiao.insert_one(mydict)

