# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import pymongo
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
client = pymongo.MongoClient(connection_string)
db = client['wooyun']
collection = db['relationships']
cl2=db['chulilist']
c1=cl2.find_one()['leixing']
cl3=db['leixing_aim']
page={"row":[]}
client = pymongo.MongoClient(connection_string)
db = client['wooyun']
weichuli = db['relationships']
chulilist=db['chulilist']

mydict={}

domain_array=[]
hrefs_s=weichuli.find()
for hrefs in hrefs_s:
    for href in hrefs['hrefs']:
        # print href
        urlsep = href.split('//')[1].split('/')[0].split('.')
        if len(urlsep)==2:
            domain=urlsep[0]+'.'+urlsep[1]
        elif len(urlsep)==1:
            pass
        else:
            domain=str(urlsep[1])+'.'+str(urlsep[2])
            # print str(domain)
        domain_array.append(domain)

num=[]
domain_array_set=[]
for id in domain_array:
    if id not in domain_array_set:
        domain_array_set.append(id)


for d in domain_array_set:
    try:
        d=str(d)
        number=domain_array.count(d)
        num.append([d,number])

    except:
        continue


print num

b=sorted(num,key=itemgetter(1,1),reverse=True)[0:9]