#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2016/7/18"
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
import time

import datetime

if __name__ == '__main__':
    while True:
        print "【执行proxy_spider 模拟脚本开始】",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        workspace="./"
        os.chdir(workspace+"proxy_spider/proxy_spider")
        os.system("python "+ "main.py")
        print "【执行proxy_spider 模拟脚本结束】",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.system("python "+ "proxy_detect.py")
        os.chdir("../../")
        os.chdir(workspace+"qb_image/qb_image")
        print "【执行qb_image 模拟脚本开始】",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.system("python "+ "main.py")
        print "【执行qb_image 模拟脚本结束】",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print "sleeping .....120 min"

        time.sleep(120*60)



