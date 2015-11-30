#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-11-5
@summary: 更新数据库中还有address地址的经纬度
@author: kanhaibo
'''
import address_to_latlnt
from pymongo import MongoClient
import threading
import multiprocessing
import time


class GeocoderToLatLnt(threading.Thread):
    '''
    @summary: 多线程转换经纬度，转换经纬度速度慢，主要是请求
    谷歌的地图api接口的时候，造成的。
    '''
    def __init__(self, threadname, db, cols):
        '''
        @summary: 初始化对象
        @param threadname:线程名称
        @param db: 数据库名称
        @param cols: 需要更新的集合
        '''
        super(GeocoderToLatLnt, self).__init__(name=threadname)
        self.db = db
        self.cols = cols

    def run(self):
        '''
        @summary: 重写父类run方法,在线程启动后执行该方法的代码
        '''
        self.collection_to_latlnt()
#         self.collection_add_column()

    def collection_add_column(self):
        conn = MongoClient('192.168.0.17:27050')
        dbTemp = conn[self.db]
        dbTemp[self.cols].update({'geometry': {'$exists': False}},
                        {'$set': {'label_flag': 0}}, multi=True)
        dbTemp[self.cols].update({'geometry': {'$exists': True}},
                {'$set': {'label_flag': 2}}, multi=True)
        conn.close()

    def collection_to_latlnt(self):
        '''
        @summary: 把传入的集合通过谷歌地图地址转成经纬度
        '''
        conn = MongoClient('192.168.0.17:27050')
        dbTemp = conn[self.db]
        addressSearch = ''
        if dbTemp[self.cols].find({'地址': {'$exists': True}}).count() > 0:
            addressSearch = '地址'
        elif dbTemp[self.cols].find({'联系地址': {'$exists': True}}).count() > 0:
            addressSearch = '联系地址'
        elif dbTemp[self.cols].find({'HeadOffice': {'$exists': True}})\
            .count() > 0:
            addressSearch = 'HeadOffice'
        elif dbTemp[self.cols].find({'Address地址': {'$exists': True}})\
            .count() > 0:
            addressSearch = 'Address地址'
        else:
            addressSearch = ''
        if addressSearch != '':
            print(self.cols + 'is activing ')
            for p in\
                dbTemp[self.cols].find({"geometry": {'$exists': False}}).\
                    batch_size(100):
                try:
                    if p[addressSearch].strip() != '':
                        try:
                            tempLatLnt = address_to_latlnt.address_to_LatLnts(
                            p[addressSearch].replace(' ', '+'))
                        except Exception as e:
                            tempLatLnt = ''
                        if tempLatLnt != '':
                            dbTemp[self.cols].update(
                                            {'_id': p['_id']},
                                            {'$set': {'geometry': tempLatLnt,
                                                      'label_flag': 2}})
                except Exception as e:
                    pass
                finally:
                    pass
            print(self.cols + 'is over ')
        conn.close()


class DisplayLatLntResults(threading.Thread):
    '''
    @summary: 得到当前库内传进来的集合中原有多少行数据，其中更新了经纬度的数据有多少
    '''
    def __init__(self, threadname, db, cols):
        '''
        @summary: 初始化对象
        @param threadname:线程名称
        @param db: 数据库名称
        @param cols: 需要更新的集合
        '''
        super(DisplayLatLntResults, self).__init__(name=threadname)
        self.db = db
        self.cols = cols

    def run(self):
        '''
        @summary: 重写父类run方法,在线程启动后执行该方法的代码
        '''
        self.display_cols_results()

    def display_cols_results(self):
        '''
        @summary: 返回集合中原有个数，以及更新的个数
        '''
        try:
            conn = MongoClient('192.168.0.17:27050')
            dbTemp = conn[self.db]
            receive_all = dbTemp[self.cols].find().count()
            receive_latlnt = dbTemp[self.cols].find(
                            {"geometry": {'$exists': True}}).count()
        except Exception as e:
            pass
        finally:
            conn.close()
#         print str(receive_all) + '+'
        print('%s中原有%d已更新%d' % (self.cols, receive_all, receive_latlnt))


# def check_googlemap_latlnt():
#     '''
#     @summary: test googlemaps googlemapsaspi
#     '''
#     conn = MongoClient('192.168.0.17:27050')
#     dbtemp = conn['cantonfair113']
#     dbtemp['113届广交会采购商名录-办公-9528'].update(
#                     {"geometry.status": 'ZERO_RESULTS'},
#                     {'$unset': {'geometry': ''}},
#                     multi=True)
#     print dbtemp['113届广交会采购商名录-办公-9528'].find(
#                     {"geometry.status": 'ZERO_RESULTS'}).count()
#     conn.close()


def main(db='cantonfair117'):
    '''
    @summary: 更新一个库内的所有集合,每个集合同时更新
    '''
    #把当前库内的集合都循环出来，放在里面里面
    temp_cols = []
    try:
        conn = MongoClient('192.168.0.17:27050')
        dbTemp = conn[db]
        cols = dbTemp.collection_names()
        for element in cols:
            if element.split('.')[0] != 'system':
                temp_cols.append(element)
    finally:
        conn.close()

    threads = []
    for m in temp_cols:
        threads.append(GeocoderToLatLnt("thread_" + str(m), db, m))
#         threads.append(DisplayLatLntResults("thread_" + str(m), db, m))
    for thread_single in threads:
        thread_single.start()
#     print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if __name__ == '__main__':
    main('cantonfair110')
#     p1 = multiprocessing.Process(target=main, args=('cantonfair116',))
#     p2 = multiprocessing.Process(target=main, args=('cantonfair115',))
#     p1.start()
#     p2.start()
