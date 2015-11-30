# -*- coding: utf-8 -*-
'''
Created on 2015-5-12

@author: kanhaibo
'''
import pymongo,logging,dict4ini
confFilePrivate='articl.conf'


class MainSource(object):
    def __init__(self,cfg):
        self.cfg=dict4ini.DictIni(confFilePrivate)
        self._rowCount=0
        self.m_cursor = None
        self.m_dbconn = None
        self.m_db = None
        #range query
        self.m_minid = 0
        self.m_maxid = 0
        self.m_start_id = 0
        #base str
        self.m_basesql_str = ''
    
    def GetScheme(self):
        '''
        获取结构，docid，文本，整数
        '''
        return[('_id',{'docid':True}),
               ('business_scope',{'type':'text'}),
               ('company',{'type':'text'}),
               ('company_address',{'type':'text'})]
    
    def GetFieldOrder(self):
        '''
        字段的优先顺序
        '''
        return[('business_scope','company_address')]
    
    def Connected(self):
        '''
        如果是数据库，则在此处做数据库连接
        '''
#         print self.cfg
#         if not self.cfg.has_key('mongodb'):
#             logging.error('Not has MongoDB info')
#             return False
        try:
            self.m_dbconn = pymongo.MongoClient(host=self.cfg.mongodb.host,\
                                               port = int(self.cfg.mongodb.port))
            self.m_db = self.m_dbconn[self.cfg.mongodb.dbname]
            self.m_db.authenticate(self.cfg.mongodb.username,self.cfg.mongodb.password)
        except pymongo.errors,e:
            logging.error("Error %d: %s" , e.args[0], e.args[1])
            return False
        return True

    def OnBeforeIndex(self):
        #select max & min doc_id
        self.m_cursor = self.m_db.enterprise.find().limit(1)
        return True
#         try:
#             self.m_cursor = self.m_dbconn.cursor()

    def NextDocument(self):
        '''
        提取正常的数据并反馈
        '''
        for mm in self.m_cursor:
            return self._getRow(mm)
    
    def _getRow(self,m_row):
#         print m_row
        self._id = m_row['_id']
        if not m_row.has_key('BUSINESS_SCOPE'):
            self.business_scope = ''
        else:    
            self.business_scope = m_row['BUSINESS_SCOPE'].encode('utf-8')
        if not m_row.has_key('COMPANY'):
            self.company = ''
        else:    
            self.company = m_row['COMPANY']     
        if not m_row.has_key('COMPANY'):
            self.company_address = ''
        else:
            self.company_address = m_row['COMPANY']
       
            
if __name__ == '__main__':
    conf = {}
    tempCount = MainSource(conf)
    tempCount.Connected()
    tempCount.OnBeforeIndex()
    tempCount.NextDocument()