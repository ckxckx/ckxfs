 # -*- coding:utf-8 -*-
from flask import *
# import json
from bson import json_util as jsonb
# from flask_bootstrap import Bootstrap
from operator import itemgetter, attrgetter
# from flask_nav import Nav
# from flask_nav.elements import *
from flask import request,session
import pymongo
import math
import re
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.contrib.fixers import ProxyFix


MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB_ckx = 'ckxlogin'
MONGODB_DB = 'wooyun'
MONGOTABLE = 'loginlist'
connection_string = "mongodb://%s:%d" % (MONGODB_SERVER, MONGODB_PORT)
MONGODB_COLLECTION_BUGS = 'wooyun_list'
MONGODB_COLLECTION_DROPS = 'wooyun_drops'
ROWS_PER_PAGE = 20




app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/index")
@app.route("/login")
@app.route("/")
def ii():
	if 'username' in session:
		return render_template('ee.html',title=u'三叶虫知识库',account=escape(session['username']))

	return render_template('jquerytry.html',title=u'三叶虫知识库')

#============注册========================
@app.route("/sign")
def signup():
    if 'username' in session:
        return u"您已经登入"
    return render_template('signup.html',title=u'三叶虫注册')
@app.route("/ckxregister",methods=['GET','POST'])
def ckxregister():
    client = pymongo.MongoClient(connection_string)
    db = client[MONGODB_DB_ckx]
    loginlist= db[MONGOTABLE]
    account = request.form['account']
    pw=request.form['passwd']
    checksentence={"account":account}
    checkname= None
    checkname = loginlist.find(checksentence)
    if checkname.count() == 0 :
        checksuccess = 'success'
        post_content={
            "account":account,
            "pw":pw,
        }
        db.loginlist.insert_one(post_content)

        return render_template('ceshil.html',content=u"注册成功")
    else:

		checksuccess= "fail"
		return u"用户已经存在"


#===================================================





 #####################写日记部分
@app.route("/drops")
def mydrops():
    if 'username' in session:
        return render_template("drops.html",account=escape(session['username']))
    else:
        return render_template("ceshil.html",content="尚未登入")

@app.route("/writedrops", methods=['GET','POST'])
def writedrops():
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)  #mongodb连接
        db = client[MONGODB_DB]  #选择mongodb数据库
        loginlist= db[MONGODB_COLLECTION_DROPS]   #选择需要的集合
        mytitle = request.form['title']
        mycontent=request.form['content']
        mytime=datetime.now()
        checksentence={"datetime":mytime,"title":mytitle,\
                       "html":mycontent,"author":escape(session['username']),\
                       "category":"原创笔记"}   #查找集合中的某一item
        checkname= None
        checkname = loginlist.find(checksentence)
        if checkname.count() == 0 :
            post_content=checksentence
            loginlist.insert_one(post_content)
            return render_template("ceshil.html", content=u"写入成功",account=escape(session['username']))
        else:
            return render_template("ceshil.html", content=u"已经存在",account=escape(session['username']))
    else:
        return render_template("ceshil.html",content="尚未登入")




###修改日记###################################3

@app.route("/mydrops/writedrops", methods=['GET','POST'])
def writedropsagain():
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[MONGODB_DB]
        loginlist= db[MONGODB_COLLECTION_DROPS]
        mytitle = request.form['title']
        mycontent=request.form['content']
        myid=request.form['myid']
        mytime=datetime.now()
        checksentence={"_id": ObjectId(myid)}
        checkname= None
        checkname = loginlist.find(checksentence)
        if checkname.count() == 0 :
            # post_content=checksentence
            # loginlist.insert_one(post_content)
            return render_template("ceshil.html", content=u"没有词条",account=escape(session['username']))
        else:
             updatesentence={ "_id":ObjectId(myid),"datetime":mytime,"title":mytitle,"html":mycontent,"author":escape(session['username']),"category":"原创笔记"}
             loginlist.update({"_id":ObjectId(myid)},updatesentence)
             return render_template("ceshil.html", content=u"已经成功修改",account=escape(session['username']))
    else:
        return render_template("ceshil.html",content="尚未登入")



# @app.route("/ee")
# def ee():
#     return render_template('ee.html',title='xxxxxxxx')

# @app.route("/lt")
# def lt():
#     return render_template('logintry.html',title='xxxxxxxx')

@app.route("/logerr")
def logerr():
    return render_template('ceshil.html',content=u"密码或账号错误")







###===========会话登陆部分--------------------------------------========

@app.route("/ckxlogin",methods=['GET','POST'])
def MockController():
	client = pymongo.MongoClient(connection_string)
	db = client[MONGODB_DB_ckx]
	loginlist= db[MONGOTABLE]
	account = request.form['account']
	pw=request.form['pw']
	checksentence={"account":account,"pw":pw}
	checkname= None
	checkname = loginlist.find(checksentence)
	if checkname.count() == 0 :
		checksuccess = 'fail'
		return redirect('/logerr')
	else:
		checksuccess= "success"
		session['username'] = request.form['account']
		return redirect('/')

	# return render_template('testf.html',account=account, pw=checkname.count())



@app.route("/lttt")
def iidex():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('ceshil.html',content=u"你还没有登入哦！")

@app.route("/404")
def iide3():
    return render_template('ceshil.html',title=u'404',account=escape(session['username']),content="404")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
	session.pop('username', None)
	return redirect('/')



#============================================================

#########################################
######################################
################################
###########################
##########################



content = {'by_bugs':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_BUGS'], 'template_html': 'search_bugs.html'},
           'by_drops':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_DROPS'], 'template_html': 'search_drops.html'},
           }


def get_search_regex(keywords, search_by_html):
    keywords_regex = {}
    kws = [ks for ks in keywords.strip().split(' ') if ks != '']
    field_name = 'html' if search_by_html else 'title'
    if len(kws) > 0:
        reg_pattern = re.compile('|'.join(kws), re.IGNORECASE)
        # keywords_regex[field_name]={'$regex':'|'.join(kws)}
        keywords_regex[field_name] = reg_pattern

    return keywords_regex


def search_mongodb(keywords, page, content_search_by, search_by_html):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    keywords_regex = get_search_regex(keywords, search_by_html)
    collection = db[content[content_search_by]['mongodb_collection']]
    # get the total count and page:
    total_rows = collection.find(keywords_regex).count()
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find(keywords_regex)\
            .sort('datetime', pymongo.DESCENDING).skip(row_start).limit(app.config['ROWS_PER_PAGE'])
        for c in cursors:
           c['datetime'] = c['datetime'].strftime('%Y-%m-%d')
           # obid=c['_id']
           if 'url' in c:
               urlsep = c['url'].split('//')[1].split('/')
               c['url_local'] = '%s-%s.html' % (urlsep[1], urlsep[2])
           page_info['rows'].append(c)
    client.close()
    #
    return page_info



################################
def search_all_mongodb(page,leixing):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    # keywords_regex = get_search_regex(keywords, search_by_html)
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    if leixing==0:
        collection = db[MONGODB_COLLECTION_BUGS ]
    else:
        collection = db[MONGODB_COLLECTION_DROPS]


    # get the total count and page:
    total_rows = collection.find().count()
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find()\
            .sort('datetime', pymongo.DESCENDING).skip(row_start).limit(app.config['ROWS_PER_PAGE'])
        for c in cursors:
           c['datetime'] = c['datetime'].strftime('%Y-%m-%d')
           # obid=c['_id']
           if 'url' in c:
               urlsep = c['url'].split('//')[1].split('/')
               c['url_local'] = '%s-%s.html' % (urlsep[1], urlsep[2])
           page_info['rows'].append(c)
    client.close()
    #
    return page_info

###############################
def search_account():

    client = pymongo.MongoClient(connection_string)
    db = client[MONGODB_DB_ckx]
    loginlist= db[MONGOTABLE]
    total_rows = loginlist.find().count()

    page_info = { 'total_rows': total_rows, 'rows': []}


    cursors = loginlist.find().sort('_id')
    for c in cursors:

       page_info['rows'].append(c)
    client.close()
    #
    return page_info






##############333333



def get_wooyun_total_count():
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    collection_bugs = db[app.config['MONGODB_COLLECTION_BUGS']]
    total_count_bugs = collection_bugs.find().count()
    collection_drops = db[app.config['MONGODB_COLLECTION_DROPS']]
    total_count_drops = collection_drops.find().count()
    client.close()

    return (total_count_bugs, total_count_drops)


@app.route('/searchindex')
def indexx():
    total_count_bugs, total_count_drops = get_wooyun_total_count()
    if 'username' in session:
        return render_template('index.html', total_count_bugs=total_count_bugs, total_count_drops=total_count_drops, title=u'知识库搜索')
    return u"尚未登入"




@app.route('/search', methods=['get'])
def search():
    if 'username' in session:
        keywords = request.args.get('keywords')
        page = int(request.args.get('page', 1))
        search_by_html = True if 'true' == request.args.get(
            'search_by_html', 'false').lower() else False
        content_search_by = request.args.get('content_search_by', 'by_bugs')
        if page < 1:
            page = 1
        #
        page_info = search_mongodb(
            keywords, page, content_search_by, search_by_html)
        #
        return render_template(content[content_search_by]['template_html'], keywords=keywords, page_info=page_info, search_by_html=search_by_html, title=u'搜索结果-知识库搜索')
    return u"尚未登入"



######日记返回#####

# @app.route('/drops/', methods=['get'])
# def search():
#     if 'username' in session:
#         obid = request.args.get('keywords')
#         page = int(request.args.get('page', 1))


@app.route('/mydrops/<objid>')
def getmydrop(objid):
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db[MONGODB_COLLECTION_DROPS ]
        # checkid={"_id":objid}
        checkid={'_id':ObjectId(objid)}
        myhtmls=collection.find(checkid)
        # my_title='444444444444'
        if myhtmls.count()==0:
            my_title="您的笔记已被外星人劫持"
        else:
            for c in myhtmls:
                my_title=c['title']
                my_html=c['html']
                drop_content="<h2>%s</h2><br><br><p>%s</p>" % (my_title,my_html)
        return render_template('dropread.html',title=u'笔记',account=escape(session['username']),content3=my_title,content2=my_html,myid=objid)
    return u"尚未登入"

    # if 'username' in session:
          # client = pymongo.MongoClient(connection_string)
          # db = client[app.config['MONGODB_DB']]
          # collection = db[MONGODB_COLLECTION_DROPS ]
          # checkid={"_id":obid}
          # myhtmls=collection.find(checkid)
          #my_title='444444444444'
          # for c in myhtmls:
          #     my_title=str(c['title'])
          #     my_html=c['html']
          # drop_content="<h2>%s</h2><br><br><p>%s</p>" % (my_title,my_html)



####返回抓取页面
@app.route('/<name>', methods=['get'])
def getmybug(name):
####注意用谷歌浏览器效果没360浏览器好
    #####方法二从数据库直接输出html
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    collection = db[MONGODB_COLLECTION_BUGS ]
    checkid={"_id":ObjectId(name)}
    myhtmls=collection.find(checkid)
    myhtml=[]
    for c in myhtmls:
        myhtml.append(c['html'])
    return myhtml[0]
    
    #方法一直接出静态文件注意app.send_static_file()方法
    # path='bugs/'+name+'.html'
    # return app.send_static_file(path)






######列表

@app.route('/buglist',methods=['get','post'])
def mybuglist():
    if 'username' in session:
        page = int(request.args.get('page', 1))
        page_info = search_all_mongodb(page,0)

        return render_template('buglist.html', keywords="****", page_info=page_info, title=u'知识库列表')

    else:
        return u"尚未登入"



@app.route('/droplist',methods=['get','post'])
def mydroplist():
    if 'username' in session:
        page = int(request.args.get('page', 1))
        page_info = search_all_mongodb(page,1)

        return render_template('droplist.html', keywords="****", page_info=page_info, title=u'知识库列表')
    else:
         return u"尚未登入"


#######################
 #####删除功能

@app.route('/deleteone/<objid>')
def deleteone(objid):
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db[MONGODB_COLLECTION_DROPS]
        # checkid={"_id":objid}
        checkid={'_id':ObjectId(objid)}
        collection.remove(checkid)
        return render_template('ceshil.html',content=u"mission complete",account=escape(session['username']))
    else:
        return u"尚未登入"



@app.route('/deleteonebug/<objid>')
def deleteonebug(objid):
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db[MONGODB_COLLECTION_BUGS]
        # checkid={"_id":objid}
        checkid={'_id':ObjectId(objid)}
        collection.remove(checkid)
        return render_template('ceshil.html',content=u"mission complete",account=escape(session['username']))
    else:
        return u"尚未登入"





###########################爬虫###########
@app.route('/crawler')
def mycrawler():
    if 'username' in session:
        mypara=u'''
ALLOWURL='http://www.freebuf.com'
STARTS_URL='http://www.freebuf.com/vuls/'
PAGE="vuls/page/%d"       ##抽取目录
XPATH1='//dl/dt/a/@href'  ##抽取目录中的url
XPATH2='//title/text()'   ##抽取标题
AUTHOR='EVIL_CALVIN'  ##操作人名称
SAVEPIC=False   ##判断是否存储图片
SPIDERNAME="freebuf"  ###爬虫名称
PAGE_MAX=1    ##抓取页数

        '''
        return render_template("crawler.html",content2=mypara, account=escape(session['username']))
    else:
        return u"尚未登入"





@app.route('/craup',methods=['post'])
def craup():
    if 'username' in session:
        me=request.form["para"]
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db["crawler_para"]
        collection.insert_one({"crawler_para":me,"uploader":escape(session['username'])})
        return render_template("ceshil.html", content=u"提交成功", account=escape(session['username']))
    else:
        return u"尚未登入"







##################################################后台

@app.route('/houtai')
def houtai():
    if 'username' in session and escape(session['username'])=="root@root":
        page_info=search_account()

        return render_template("accountmanage.html",page_info=page_info,account=escape(session['username']))
    else:
        return u"未授权"



##########################
@app.route('/deleteaccount/<objid>')
def deleteaccount(objid):
    if 'username' in session and escape(session['username'])=="root@root":
        client = pymongo.MongoClient(connection_string)
        db = client[MONGODB_DB_ckx]
        loginlist= db[MONGOTABLE]
        loginlist.remove({"_id":ObjectId(objid)})
        return render_template("ceshil.html",content=u"账号删除成功",account=escape(session['username']))
    else:
        return u"未授权"
######################################-----------------
# @app.route('/deleteone/<objid>')
# def deleteone():
#     if 'username' in session:
#         pass
#     else:
#         return u"尚未登入"










#########################advanced hacking##########33

@app.route('/relation_1',methods=['get','post'])
def relation_1():
    if 'username' in session:
        page = int(request.args.get('page', 1))
        page_info = search_all_mongodb(page,0)

        return render_template('relation_1.html', account=escape(session['username']))

    else:
        return u"尚未登入"



#########################advanced hacking##########33

@app.route('/relation_uploader_1',methods=['get','post'])
def relation_uploader_1():
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client['wooyun']
        cl=db["uploader_aim"]
        number=cl.count()
        kkk=cl.find().sort('renqi', pymongo.DESCENDING)
        page_info = {'total_rows': number, 'rows':[]}
        for kk in kkk:
            print kk
            page_info['rows'].append(kk)
        return render_template('hacklist.html', page_info=page_info,account=escape(session['username']))

    else:
        return u"尚未登入"







@app.route('/upinfo/<objid>')
def getmyuploader(objid):
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db['uploader_aim']
        # checkid={"_id":objid}
        checkid={'_id':ObjectId(objid)}
        results=collection.find_one(checkid)

        return render_template('updangan.html',title=u'档案馆', page=results,account=escape(session['username']))


@app.route('/relation_leixing_1')
def getmyleixing():
    if 'username' in session:
        client = pymongo.MongoClient(connection_string)
        db = client[app.config['MONGODB_DB']]
        collection = db['relationships']
        cl2=db['chulilist']
        c1=cl2.find_one()['leixing']
        cl3=db['leixing_aim']
        page={"row":[]}
        for key in c1:

        # checkid={"_id":objid}
            checkid={'leixing':key}
            results=collection.count(checkid)
            cc=cl3.find_one({"leixing":key})
            page['row'].append({"leixing":key,"cishu":results,"wenzhang":cc['titles']
                                ,"uploaders":cc["uploaders"]
                                })

        # return str(page['row'])

        return render_template('leixing.html',title=u'档案馆', page=page,account=escape(session['username']))



    return u"尚未登入"






@app.route('/relation_urls_1')
def getmyurls():
    if 'username' in session:
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
            num.append([str(d),number])

        b=sorted(num,key=itemgetter(1,1),reverse=True)[0:9]

        # b=db["url_aim"].find_one()["shuzu"][0:1]

        return render_template('getmyurls.html',title=u'档案馆', name=b,account=escape(session['username']))
    return u"尚未登入"


@app.route('/date_relate')
def getmydate():
    if 'username' in session:
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
            rongqi3.append([rongqi1])

        # print rongqi3


        return render_template("date_relate.html",info=info,rongqi3=rongqi3,account=escape(session['username']))
    else:
        return u"未授权"





app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
	# app.run(host='0.0.0.0',port='80')
    app.run(debug=True)
