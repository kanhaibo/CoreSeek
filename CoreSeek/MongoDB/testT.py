# -*- coding: utf-8 -*-
'''
Created on 2015-6-2

@author: kanhaibo
'''
import urllib2,json,urllib
#http://192.168.100.15:8000/enterprise?query=海波&limit=1&offset=0&sort=sortid desc

def getPushResult(url):
    params = {}
    params["query"] = "海波"
    params["limit"] = 1
    params["offset"] = 1
    rep = httpPost(url,params)
    return rep

def httpPost(url, params):
#     data_json = json.dumps(params)
#     print type(data_json)
#     print data_json
#     url = 'http://127.0.0.1:8000/enterprise'
    req = urllib2.Request(urllib.quote(url,":/=?&"))
    res_stream = urllib2.urlopen(req, timeout = 60)
    page_str = res_stream.read()
    page_dict = eval(page_str)
#     print page_dict
    return page_dict


if __name__ == '__main__':
    print getPushResult("http://192.168.0.32:8000/enterprise?query=炉&limit=1")