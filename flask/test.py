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
page=[]
client = pymongo.MongoClient(connection_string)
db = client['wooyun']
weichuli = db['relationships']
chulilist=db['chulilist']
cl=db['riqi_leixing_guanlian']
riqishu=chulilist.find_one()['riqi']
page=[]
riqishu=sorted(riqishu)
for riqi in riqishu:
    zongcishu=cl.count({"date":riqi})
    leis=[]

    for lx in cl.find({"date":riqi}):
        leis.append(lx['leixing'])

    a = []
    for i in set(leis):
        if leis.count(i)>0:
            print i
            a.append([i,leis.count(i)])

    page.append([riqi,zongcishu,a])

print page
xzhou=[]
yzhou=[]
rongqi=[]
for ite in page:
    xzhou.append(str(ite[0]))
    yzhou.append(ite[1])
    # rongqi.append()
info=[xzhou,yzhou]

rongqi3=[]
leixingshu=chulilist.find_one()['leixing']
for leixing in leixingshu:
    rongqi1=[]
    rongqi2=[]
    for riqi in riqishu:
        num=cl.count({"leixing":leixing,"date":riqi})
        rongqi1.append(num)
        rongqi2.append(str(riqi))
    leixing=str(leixing)
    rongqi3.append([leixing,rongqi2,rongqi1])

print rongqi3