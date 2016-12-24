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


ok=db['chulilist'].find_one({"_id" : ObjectId("585d36ec2514971ea8747224")})
for name in ok["uploaders"]:


    uploader=name
    checkname = weichuli.find({"uploader":uploader})
    mydict={}
    items_title=[]
    items_leixing=[]
    items_riqi=[]
    items_hrefs=[]
    renqi=0
    for it in checkname:
        items_title.append(it["title"])
        items_leixing+=it["leixing"]
        items_riqi.append(it["riqi"])
        renqi+=int(it["weiguan"])
        items_hrefs+=it["hrefs"]
    mydict["uploader"]=uploader
    mydict["titles"]=items_title
    mydict["leixing"]=list(set(items_leixing))   #删除数组中重复部分
    mydict["renqi"]=renqi
    mydict["riqi"]=items_riqi
    mydict["zongshu"]=weichuli.count({"uploader":uploader})
    mydict["hrefs"]=list(set(items_hrefs))
    chuliname.insert_one(mydict)
