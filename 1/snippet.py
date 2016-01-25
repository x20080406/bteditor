#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 10 Aug 2014 17:04:23

@author: tianjie
'''



import bencode

def torrent2dict(filename):
    f = open(filename, 'rb')
    s = f.read()
    f.close()
    d = bencode.bdecode(s)
    return d

#http://www.verydemo.com/cj.jsp?c=16&u=li-yong-python-de-bittorrent-kuo-zhan-ku-jie-xi-bittorrent-wen-jian
#/home/tianjie/Desktop/udx/aff181394b7d9f0f61a2b392707b12485110008a.torrent
if __name__ == "__main__":
    #fdat = raw_input('please input the torrent file path:')
    #print '================================= ', fdat , '========================================='
    #fdat='/media/tianjie/EC2892B628927F70/Documents and Settings/Administrator/桌面/udx/2e2be29b7678453ad30dc644bb6a30110411f0b4.torrent'
    fdat='/home/tianjie/Desktop/a111.torrent'
    d = torrent2dict(fdat)
    for k in d.keys():
        if k == 'info':
            continue            
        print k , ' : ' , d[k]
    
    info = d.get('info')
    info.pop('publisher.utf-8',None)
    info.pop('name.utf-8',None)
    info.pop('publisher-url.utf-8',None)
    
    for k in info.keys():
        if k == 'pieces':
            print k, ' : ...'
            continue
        if k=='files':
            i=0
            for item in info[k]:
                for z in item.keys():
                    i+=1
                    item['id']=i
                    '''
                    if z =='path' and item[z][0].endswith('mp4'): 
                        print z, ' ==>: ', item[z][0]
                    else:
                        item.pop(z,None)
                        #print z, ' ==>: ', info[k][0][z]  
                        #print ''
                    ''' 
        else :
            print k, ' : ', info[k]
    
    nf = open('/home/tianjie/Desktop/a111.torrent','w')
    nf.write(bencode.bencode(d));
    nf.close()
