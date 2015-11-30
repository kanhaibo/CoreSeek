# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: kanhaibo
'''
import pymongo,dict4ini
confFilePrivate='articl.conf'

class MainSource(object):
    def __init__(self,conf):
        self.conf = conf
        self.idx = 0
        self.conn = None
        self.cur = None
        self.data = []
        self.cfg=dict4ini.DictIni(confFilePrivate)
        
    def GetScheme(self):
        return [
                ('_id',{'docid':True}),
                ('business_scope',{'type':'text'}),
                ]
    
    def GetFieldOrder(self):
        return [('business_scope'),]
    
    def Connected(self):
        if self.conn == None:
            self.conn = pymongo.MongoClient(host=self.cfg.mongodb.host,\
                                               port = int(self.cfg.mongodb.port))
        mydb = self.conn[self.cfg.mongodb.dbname]
        mydb.authenticate(self.cfg.mongodb.username,self.cfg.mongodb.password)
        mchinatsi = mydb.chinatsi
        self.cur = mchinatsi.find()
        size = self.cur.count()
        self.data = range(size)
        
    def NextDocument(self):
        if self.idx < len(self.data):
            item = self.cur.next()
            self._id = item["_id"]
            self.business_scope = item['business_scope'].encode('utf-8')
            self.idx += 1
            return True
        else:
            return False    


if __name__ == '__main__':
    pass