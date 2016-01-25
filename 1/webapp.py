#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 10 Aug 2014 15:53:40

@author: tianjie
'''
import sys
import os
from datetime import timedelta

abspath = os.path.abspath(__file__)
app_root = os.path.dirname(abspath)
#path = os.path.join(app_root, 'lib/python2.7/site-packages')
#sys.path.insert(0, path)
#sys.path.insert(0, app_root)
#sys.path.insert(0, '/home/tianjie/pyworkspace/bteditor/lib')
#sys.path.insert(0, app_root)
from flask import Flask,session
from flask_session import Session

app = Flask(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')
app.config['SESSION_TYPE'] = 'kvdb'
Session(app)

session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=5)

from bteditor.controller import *

#app.add_url_rule('/', view_func=index)

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)