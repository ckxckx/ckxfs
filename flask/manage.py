# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from app import app

manager = Manager(app)

# @manager.command
# def hello():
#     print "hello"



@manager.option('-n', '--name', help='Your name')
def hello(name):
    print "hello", name

if __name__ == "__main__":
    manager.run()