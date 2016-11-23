配置说明：

本应用可以在跨平台运行，由python解释器作为编程支持。

1：flask配置
在当前目录下进入命令行，
pip install -r note_requirements.txt

2：scrapy安装：
参照网址
on ubuntu
http://scrapy-chs.readthedocs.io/zh_CN/stable/topics/ubuntu.html

windows 同理

3：mongodb 安装以及服务设置
on windows:
下载地址：http://www.mongodb.org/downloads 
Java代码  收藏代码
2、解压并且重命名为mongodb，copy到D:/websoft/下，注：这个是我的命名及其目录结构,可以根据你自己的习惯执行  
3、在mongodb文件件下，新建两个文件data和logs  
4、配置mongodb服务器：  
4.1 cmd进入到：D:/websoft/mongodb/bin下（操作：1.d:  2.cd :/websoft/mongodb/bin）;  
4.2 命令：mongod --dbpath d:/websoft/mongodb/data  
   打印如下后：  


命令行下运行 MongoDB 服务器
为了从命令提示符下运行MongoDB服务器，你必须从MongoDB目录的bin目录中执行mongod.exe文件。
mongod.exe --dbpath c:\data\db

设置成服务（开机启动）得用管理员的cmd（注意）：
mongod.exe --logpath "C:\data\dbConf\mongodb.log" --logappend --dbpath "C:\data\db"  --serviceName MongoDB -install 



on ubuntu：

详见：
http://jingyan.baidu.com/article/9158e0003555a1a2541228e1.html?qq-pf-to=pcqq.c2c





**************************************************************************************
***************************服务器架设*************************************************
**************************************************************************************

这个只针对linux系统：
可以用virtualenv，但这里不说明：

sudo apt-get install python-virtualenv python-pip
sudo pip install gunicorn
sudo apt-get install nginx


然后：
gedit /etc/nginx/sites-available/mynoteapp.conf
写入，保存（以下根据需要更改）
server {
    listen 80;
    server_name hello.itu24.com;
 
    root /path/to/mynoteapp;
 
    access_log /path/to/mynoteapp/logs/access.log;
    error_log /path/to/mynoteapp/logs/error.log;
 
    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }
}



删除：
rm /etc/nginx/sites-available/default.conf




sudo ln -s /etc/nginx/sites-available/mynoteapp.conf /etc/nginx/sites-enabled/

用以下命令查看nginx是否正确配置
nginx -t

如果正确，重启nginx：

sudo service nginx reload

cd 到网络应用的目录下（app.py）
gunicorn app:app

第一个app是app.py的名字，第二个是其中的app对象



然后打开浏览器可以看到结果



**************************************************************************
**************************************************************************


添加爬虫：
在/scrapy/wooyun/
路径下scrapy crawl freebuf 进行抓取，抓取控制参数详见脚本