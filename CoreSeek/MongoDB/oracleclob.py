# -*- coding: utf-8 -*-
'''
Created on 2015-5-15
@author: kanhaibo
'''
import dict4ini
import cx_Oracle
import os
confFilePrivate = 'articl.conf'
#解决中文乱码问题
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class MainSource(object):
    def __init__(self, conf):
        self.conf = conf
        self.idx = 0
        self.conn = None
        self.cur = None
        self.curCount = None
        self.size = 0
        self.data = []
        self.cfg = dict4ini.DictIni(confFilePrivate)

    def GetScheme(self):
        return [
                ('newsid', {'docid':True}),
                ('content', {'type':'text'}),
                ]

    def GetFieldOrder(self):
        return [('content'), ]

    def Connected(self):
        if self.conn == None:
            strConn = self.cfg.oracle.username + '/' + self.cfg.oracle.password
            +'@'+self.cfg.oracle.host+':'+str(self.cfg.oracle.port)+'/'+self.cfg.oracle.dbname
            self.conn = cx_Oracle.connect(strConn)
#             tns=cx_Oracle.makedsn(self.cfg.oracle.host,self.cfg.oracle.port,self.cfg.oracle.dbname)
#             self.conn=cx_Oracle.connect(self.cfg.oracle.username,self.cfg.oracle.password,tns)
            self.cur=self.conn.cursor()
            self.curCount = self.conn.cursor()
        self.curCount.execute('select count(1) from news ')
        self.size = self.curCount.fetchone()
        print self.size[0]
        self.cur.execute('select newsid , content from news ')
#         rs = self.cur.fetchone()
#         print len(rs)
#         tempStr = rs[0][1].read()
#         print tempStr
#         size = self.cur.count()
#         self.data = range(size)
        
    def NextDocument(self):
        if self.idx < self.size[0]:
            item = self.cur.fetchone()
            self.newsid = item[0]
            try:
                self.content = item[1].read()
            except:
                self.content = ''
            self.idx += 1
            return True
        else:
            return False    


if __name__ == '__main__':
    conf = {}
    tempCount = MainSource(conf)
    tempCount.Connected()
    tempCount.NextDocument()