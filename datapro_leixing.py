# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
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
chuliname=db['leixing_aim']


ok=db['chulilist'].find_one({"_id" : ObjectId("585d36ec2514971ea8747224")})
for leixing in ok["leixing"]:

    checkname = weichuli.find({"leixing":leixing})
    mydict={}
    items_title=[]
    items_uploaders=[]
    renqi=0
    for it in checkname:
        items_title.append(it["title"])
        items_uploaders.append(it["uploader"])

    mydict["uploaders"]=items_uploaders
    mydict["titles"]=items_title
    mydict["leixing"]=leixing
    # mydict["zongshu"]=

    chuliname.insert_one(mydict)

