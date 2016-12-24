# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
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
domain_array_set=set(domain_array)
for d in domain_array_set:
    number=domain_array.count(d)
    num.append([d,number])

print "zuizhong"
# print num

b=sorted(num,key=itemgetter(1,1),reverse=True)


print b
mm={}
mm["shuzu"]=b
db['url_aim'].insert(mm)


