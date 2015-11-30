#coding:utf-8
'''
created 2015-5-27
@author: kanhaibo
'''


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from sphinxapi import *
import sys, time
import datetime,calendar
import json
import urllib


from tornado.options import define,options
define("port",default=8000,help="run on the given port ",type=int)


def coreseekQueryEnterprise(index='python_enterprise_business',q='钢铁',offset=0,limit=10,sortby= '@weight desc'):
    mode = SPH_MATCH_PHRASE
    host = '192.168.0.17'
    port = 30001
    filtercol = ''
    filtervals = []
    #年月日时分秒
#     dateandtimelow = datetime.datetime(2013,9,5,11,00,00)
#     dateandtimeup = datetime.datetime(2014,9,5,11,00,00)
#     filterrange = True
    sortby = '@weight desc'
    groupby = ''
    groupsort = '@group desc'
#     limit = 0
    # do query
    cl = SphinxClient()
    cl.SetServer ( host, port )
    cl.SetWeights ( [100, 1] )
    cl.SetMatchMode ( mode )
    if filtervals:
        cl.SetFilter ( filtercol, filtervals )
#     if filterrange:
#         cl.SetFilterRange('dateandtime',int(time.mktime(dateandtimelow.timetuple())),int(time.mktime(dateandtimeup.timetuple())))
    if groupby:
        cl.SetGroupBy ( groupby, SPH_GROUPBY_ATTR, groupsort )
    if sortby:
        cl.SetSortMode ( SPH_SORT_EXTENDED, sortby )
    if limit:
        cl.SetLimits ( offset, limit, max(limit,1000) )
    res = cl.Query ( q, index )
    if not res:
        return'query failed: %s' % cl.GetLastError()
    else:
        if res.has_key('matches'):
            res['matches'].append({'total':res['total_found']})
            return res['matches']
        else:
            return ''

    
def coreseekQueryOracleClob(index='python_oracleclob',q='钢铁',offset=0,limit=10,sortby= '@weight desc ,dateandtime desc'):
#     q = '钢铁'
    # mode = SPH_MATCH_ALL
    mode = SPH_MATCH_PHRASE
    host = '192.168.0.17'
    port = 30001
    filtercol = ''
    filtervals = []
    #年月日时分秒
    dateandtimelow = datetime.datetime(2013,9,5,11,00,00)
    dateandtimeup = datetime.datetime(2014,9,5,11,00,00)
    filterrange = True
#     sortby = '@weight desc ,dateandtime desc'
    groupby = ''
    groupsort = '@group desc'
#     limit = 0
    # do query
    cl = SphinxClient()
    cl.SetServer ( host, port )
    cl.SetWeights ( [100, 1] )
    cl.SetMatchMode ( mode )
    if filtervals:
        cl.SetFilter ( filtercol, filtervals )
    if filterrange:
        cl.SetFilterRange('dateandtime',int(time.mktime(dateandtimelow.timetuple())),int(time.mktime(dateandtimeup.timetuple())))
    if groupby:
        cl.SetGroupBy ( groupby, SPH_GROUPBY_ATTR, groupsort )
    if sortby:
        cl.SetSortMode ( SPH_SORT_EXTENDED, sortby )
    if limit:
        cl.SetLimits ( offset, limit, max(limit,1000) )
    res = cl.Query ( q, index )
    if not res:
        return'query failed: %s' % cl.GetLastError()
    else:
        if res.has_key('matches'):
            res['matches'].append({'total':res['total_found']})
            return res['matches']
        else:
            return ''


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        coreseekquery = self.get_argument('query','唐宋').encode('utf-8')
        coreseeklimit = int(self.get_argument('limit',10))
        coreseeksort = self.get_argument('sort','@weight desc').encode('utf-8')
        result = coreseekQueryOracleClob(q = coreseekquery,limit = coreseeklimit,sortby = coreseeksort)
        self.write(json.dumps(result))
    def post(self):
        self.get()
            

class EnterpriseHandler(tornado.web.RequestHandler):
    def get(self):
        coreseekquery = self.get_argument('query','钢').encode('utf-8')
#         print urllib.unquote(coreseekquery)
        coreseeklimit = int(self.get_argument('limit',10))
#         print coreseekquery
        coreseeksort = self.get_argument('sort','@weight desc').decode('utf-8').encode('utf-8')
        result = coreseekQueryEnterprise(q = coreseekquery,limit = coreseeklimit,sortby = coreseeksort)
        self.write(json.dumps(result))
    def post(self):
        self.get()
        
        
if __name__=="__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/oracleclob", IndexHandler),(r"/enterprise",EnterpriseHandler),])
    http_server  = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()