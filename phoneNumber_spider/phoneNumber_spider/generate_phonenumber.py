#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2016/9/3"
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
import json
import os
import sys

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


def read_lines(file_path):
    file = open(file_path)
    city_phones = {}
    while 1:
        line = file.readline()
        if line:
            city_phone_dict = json.loads(line)
            city_name =city_phone_dict['capital'] +"_"+ city_phone_dict['city_name']
            prefix_list = city_phone_dict['prefix_list']
            if city_name in city_phones:
                city_phones[city_name].append(prefix_list)
            else:
                city_phones[city_name] = []
                city_phones[city_name].append(prefix_list)
        if not line:
            break
    return city_phones


def save_phone_number(content, name):
    fileName = name + ".txt"
    if os.path.isfile(file_name):
        return
    with open(fileName, 'w') as f:
        print u"正在偷偷保存信息为", fileName
        f.write(content.encode('utf-8'))


def generate_phone(prefix_list):
    content = ""
    for prefix in prefix_list:
        for i in range(9999):
            phone_number = str(prefix) + "{:0>4d}".format(i)
            content += phone_number + "\r"
    return content


def make_dir(floder_path, localpath):
    try:
        os.mkdir(localpath)
    except:
        pass
    try:
        capital_name=floder_path.split("_")[0]
        city_name=floder_path.split("_")[1]
        if os.path.isdir(os.path.join(localpath, capital_name)):
            pass
        else:
            os.mkdir(os.path.join(localpath, capital_name))
        if os.path.isdir(os.path.join(localpath, capital_name,city_name)):
            return
        os.mkdir(os.path.join(localpath, capital_name,city_name))
    except:
        pass

if __name__ == "__main__":
    localpath = "./phone_number"
    city_phones = read_lines("./phone.json")
    for key, value in city_phones.items():
        make_dir(key, localpath)
        for item in value:
            file_name=item[0][0:3]+"xxxx"
            content=generate_phone(item)
            path=key.split("_")
            save_phone_number(content,os.path.join(localpath,path[0],path[1],file_name))
