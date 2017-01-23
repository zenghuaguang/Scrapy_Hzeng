#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2016/9/1"
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
import sys

import re
from scrapy import Spider, Selector, Request
from qb_image.items import QbImageItem, HbImageItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


class HbImageSpider(Spider):
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "huaban_image"
    allowed_domains = ["huaban.com"]
    start_urls = [
        "http://huaban.com/favorite/beauty/"
    ]
    count = 0
    def parse(self, response):
        host="http://huaban.com/pins/"
        img_host="http://img.hb.aicdn.com/"
        sites=response.body.split("\n")
        for site in sites:
            site=site.strip().strip(';')
            if site.startswith('app.page["pins"]'):
                json_str=site.split('=',1)[-1]
                image_items=json.loads(json_str)
                for item in image_items:
                    hb_item=HbImageItem()
                    print item['pin_id']
                    hb_item['pin_id']=str(item['pin_id'])
                    hb_item['image_url']=img_host+item['file']['key']
                    yield hb_item
                    # url=host+str(item['pin_id'])
                    # yield Request(url,meta={"item" : hb_item},callback=self.parse_img)


    def parse_img(self, response):
        item = response.meta['item']
        yield  item


