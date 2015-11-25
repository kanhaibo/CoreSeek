#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-11-24
@summary: 宏观数据里面巴基斯坦各个集合的操作
@author: kanhaibo
'''
from mongoengine import *
import json
import datetime
from __future__ import unicode_literals

connect(alias='country_pakistan', host='mongodb://192.168.0.17:27050/巴基斯坦')


class cpi(DynamicDocument):
    '''
    @summary: 居民消费价格指数
    @param Date: 指当前日期，主要是以月为单位
    '''
    Date = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now())
    meta = {'db_alias': 'country_pakistan'}

    def clean(self):
        self.date = datetime.datetime.strptime(self.Date, '%Y/%m/%d')


def oper_cpi():
    '''
   @summary: 新增转换，把数据类型是文本类型的进行时间类型转换转换
    '''
    for m in cpi.objects():
        m.save()


class gdp(DynamicDocument):
    Date = StringField()
    date = DateTimeField()
    meta = {'db_alias': 'country_pakistan'}

    def clean(self):
        self.date = datetime.datetime.strptime(self.Date, '%Y/%m/%d')


def oper_gdp():
    for m in gdp.objects():
        m.save()


if __name__ == '__main__':
    pass
#     oper_cpi()
#     oper_gdp() = 'sdfds'
