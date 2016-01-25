#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys,sae ,os
from datetime import timedelta

# abspath = os.path.abspath(__file__)
#app_root = os.path.dirname(__file__)
#path = os.path.join(app_root, 'site-packages')

# sys.path.insert(0, app_root)
# sys.path.insert(0, path)

from flask import Flask
from flask_session import Session
app = Flask(__name__)
 
reload(sys)
sys.path.insert(0, "site-packages")
sys.setdefaultencoding('utf-8')
#app.config['SESSION_TYPE'] = 'kvdb'
app.config['SECRET_KEY'] = 'this is a secret key'
#import pdb
#pdb.set_trace()
app.permanent_session_lifetime = timedelta(seconds=20)

sess = Session()
sess.init_app(app)

from bteditor.controller import *
#app.debug =True

application= sae.create_wsgi_app(app)

#if __name__ == '__main__':
    #app.run()
#    app.run(debug=True)
