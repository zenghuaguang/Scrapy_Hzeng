#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2017/1/7"
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
import os
import sys
import unittest
import urllib

import multiprocessing
import requests
from pymongo import MongoClient

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


url = "http://ip.cn"

def db_help():
    server = '10.200.10.224'
    port = 27017
    db = 'proxy_db'
    col = 'proxy_ip'
    connection = MongoClient(server,port)
    db = connection[db]
    return db[col]

def detect( proxys):
    '''
    http://www.baidu.com  作为检测目标
    :return:
    '''
    badNum = 0
    goodNum = 0
    for proxy in proxys:
        ip = proxy['host']
        port = proxy['port']
        try:
            proxy_host = proxy['type'].lower() + "://" + ip + ':' + port  #
            response = requests.get(url, proxies={proxy['type'].lower(): proxy_host}, timeout=5)
            if response.status_code != 200:
                db_help().delete_many({'host': ip, 'port': port})
                badNum += 1
                print os.getpid(),proxy_host, 'bad proxy'
            else:
                goodNum += 1
                print os.getpid(),proxy_host, 'success proxy'
        except Exception, e:
            print os.getpid(),proxy_host, 'bad proxy'
            db_help().delete_many({'host': ip, 'port': port})
            badNum += 1
            continue


def test_main():
    step = 5
    proxys = []
    proxys_docs =db_help().find()
    for doc in proxys_docs:
        proxys.append(dict(doc))
    proxys_items = [proxys[i:i + step] for i in xrange(0, len(proxys), step)]
    pool = multiprocessing.Pool(processes = 10)
    for proxy_list in proxys_items:
        pool.apply_async(detect, (proxy_list, ))
    pool.close()
    pool.join()
    print  "end"


if __name__ == "__main__":
    test_main()
