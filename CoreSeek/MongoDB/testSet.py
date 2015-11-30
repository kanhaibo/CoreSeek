# -*- coding: utf-8 -*-
'''
Created on 2015-6-3

@author: kanhaibo
'''
import time


if __name__ == '__main__':
    m  = []
    l  = []
    for i in range(1,10000000):
        m.append(i)
        l.append(i+50)
    a = set(m)
    b = set(l)
    ll =  time.time()
    print ll
    print a - b
    print   time.time() - ll      