#!/usr/bin/env python
# coding: utf-8
# -*- coding:utf-8 -*-

from common import app,mailp,mailu,mailr
from flask import (render_template as view, request,session ,redirect,make_response,current_app)
from random import Random
import bencode
import sae.kvdb

kv = sae.kvdb.KVClient()

@app.route('/', methods=['GET', 'POST'])
def index():
    return view("bteditor/index.html")

@app.route('/edit', methods=['POST'])
def edit():
    rs = {}
    files=[]
    rs['files']=files
    try:
        if request.content_length > 300*1024:
            return view("bteditor/index.html",msg="文件太大，不要超过300kb！")
        
        _file= request.files['torrent']
        _filename=_file.filename;
        if(_filename.endswith('.torrent')==False):
            return view("bteditor/index.html",msg="上传的文件不对！请重新上传！")
            
        
        _dict = bencode.bdecode(_file.read())
        info = _dict.get('info')
        
        info.pop('publisher.utf-8',None)
        info.pop('name.utf-8',None)
        info.pop('publisher-url.utf-8',None)

        i=1
        for k in info.keys():
            import pdb
            if k == 'files' or k =='name':
                if k== 'name':
                    rs['name']=info[k]
                else:
                    for _file in info[k]:
                        #pdb.set_trace()
                        #if _file['path'] == None or _file['path'][0].strip() == '':
                        #    continue 
                        _file['id'] = i
                        #if _file['path'][0].startswith('_____padding_file') == False:
                        files.append(_file)
                        i+=1
        cid = random_str(16)
        kv.set(cid,_dict,app.permanent_session_lifetime.total_seconds())
        
        _view = view("bteditor/edit.html",p = rs)
        res = make_response( _view )
        res.set_cookie(app.session_cookie_name,cid)
        return res
    except ValueError:
        #return view("bteditor/index.html",err=ValueError)
        raise ValueError


@app.route('/fresh', methods=['POST'])
def fresh():
    _dict = None
    cid = request.cookies.get(app.session_cookie_name)
    if cid is None:
    	return  view("bteditor/index.html",msg="时间久远，没有东西可下,快去编辑种子吧")
 
    cid=str(cid)
    _dict=kv.get( cid )
    
    if _dict is None:
        return  view("bteditor/index.html",msg='时间久远，没有东西可下,快去编辑种子吧')
    
    info = _dict.get('info')
    
    for k in info.keys():
        if k == 'files' or k =='name':
            if k == 'name':
                info[k]=str(request.form['name'])
            else:
                for _file in info[k]:
                    if _file['id'] == None :
                        continue
                    if _file.has_key('path.utf-8'):
                        _file.pop('path.utf-8')
                    if request.form.get('f'+str(_file['id'])) is None:
                        _len = len(_file['path'])
                        del _file['path'][0:_len]
                        _file['path'].append(' ')
                        #info['files'].remove(_file)
                        #del _file
                    else:
                        del _file['path'][0:len(_file['path'])]
                        _file['path']=str(request.form.get('f'+str(_file['id']))).split('/')
                        _file.pop('id')
    
    info = kv.get_info()
    kv.set(cid,_dict,app.permanent_session_lifetime.total_seconds()) 
    return redirect("./finish")

@app.route('/finish', methods=['get'])
def finish():
    cid = request.cookies.get(app.session_cookie_name)
    if cid is None:
        return view("bteditor/index.html",msg='时间久远，没有东西可下,快去编辑种子吧')
    
    cid=str(cid)
    _dict=kv.get(cid)
    
    if _dict is None:
        return view("bteditor/index.html",msg="时间久远，没有东西可下,快去编辑种子吧")
    
    return view("bteditor/finish.html")

@app.route('/download', methods=['get'])
def download():
    cid = request.cookies.get(app.session_cookie_name)
    if cid is None:
        return view("bteditor/index.html")
    
    cid=str(cid)

    _dict=kv.get(cid)
    
    if _dict is None:
        return view("bteditor/index.html",msg="时间久远，没有东西可下,快去编辑种子吧")
    
    response = make_response(bencode.bencode(_dict))
    response.headers["Content-Disposition"] = "attachment; filename="+cid+".torrent"
    kv.delete(cid)
    return response

@app.route('/help', methods=['get'])
def help():
    return view("bteditor/help.html")



def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
