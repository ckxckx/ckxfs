# -*- coding: utf-8 -*-
#这段代码将relationship中的爬取部分重要的部分分离开来做统一归纳
# -*- coding: utf-8 -*-
import pymongo;


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


tongji = weichuli.find()
tongjidict={}
items_names=[]
items_leixings=[]
items_urls=[]
items_titles=[]
items_riqis=[]
renqi=0
for it in tongji:
    items_names.append(it["uploader"])
    items_titles.append(it["title"])
    items_leixings+=it["leixing"]
    items_riqis.append(it["riqi"])
    # items_leixings+=it["leixing"]
    items_urls+=it["hrefs"]

tongjidict["uploaders"]=list(set(items_names))
tongjidict["titles"]=list(set(items_titles))
tongjidict["leixing"]=list(set(items_leixings))   #删除数组中重复部分
# tongjidict["renqi"]=renqi
tongjidict["riqi"]=list(set(items_riqis))
chulilist.insert_one(tongjidict)
#
# for my in tongjidict["riqi"]:
#     print my

