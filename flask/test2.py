# -*- coding: utf-8 -*-

import pymongo
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
client = pymongo.MongoClient(connection_string)
db = client['wooyun']
collection = db['relationships']
cl2=db['chulilist']
c1=cl2.find_one()['leixing']
cl3=db['leixing_aim']
page={"row":[]}
for key in c1:

# checkid={"_id":objid}
    checkid={'leixing':key}
    results=collection.count(checkid)
    print results
    cc=cl3.find_one({"leixing":key})
    print cc["leixing"]
    # page['row'].append({"leixing":key,"cishu":results,"wenzhang":cc['titles']
    #                     ,"uploaders":cc["uploaders"]
    #                     })
# print page