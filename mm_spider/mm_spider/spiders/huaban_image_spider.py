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
import logging
import sys
import re
from scrapy import Spider, Selector, Request
from mm_spider.items import MmSpiderItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')
'''
{
  "expires_in": 2592000,
  "refresh_token": "22.46e3dad8d3296ccfd66b74bfa4775527.315360000.1800169524.1142366778-9221408",
  "access_token": "21.4648aa9c20aa9e29f2adcf50802f97a8.2592000.1487401524.1142366778-9221408",
  "session_secret": "28a9353539007e3af9ec3082215438bc",
  "session_key": "9mnRcAB1toUuhIxZXZmNMPE3JIRJAN/5kUpFT+Ms6y1tmo80AjYHEvLYqTFckGmvc2UNkRAmaAwYt9Mn6MJYbN7VQpMcTEOj2A==",
  "scope": "basic"
}
'''

class HbImageSpider(Spider):
    logger=logging.getLogger()
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "huaban_boards"
    allowed_domains = ["huaban.com"]
    start_urls = [
        "http://huaban.com/boards/favorite/beauty/"
    ]

    def parse(self, response):
        if "board_count" in response.meta:
            board_count = response.meta['board_count']
        else:
            board_count=0
        board_host = "http://huaban.com/boards/{0}/"
        next_url=response.url.split("?")[0]+"?iy2n3lr1&max={0}&limit=20&wfl=1"
        sites = response.body.split("\n")
        max_page=10
        min_board_id=0
        for site in sites:
            site = site.strip().strip(';')
            if site.startswith('app.page["boards"]'):
                json_str = site.split('=', 1)[-1]
                board_items = json.loads(json_str)
                for item in board_items:
                    print item['board_id']
                    if min_board_id == 0 or min_board_id > item['board_id']:
                        min_board_id=item['board_id']
                    url = board_host.format(item['board_id'])
                    yield Request(url, meta={"count": 0,"max_page":max_page}, callback=self.parse_board)
        board_count+=1
        board_url=next_url.format(min_board_id)
        if board_count==3:
            return
        yield Request(board_url, meta={"board_count": board_count}, callback=self.parse)


    def parse_board(self, response):
        self.logger.info('url:{0}'.format( response.url))
        board_host = "http://huaban.com/boards/{0}/?iy2bf9u4&max={1}&limit=20&wfl=1"
        img_host = "http://img.hb.aicdn.com/"
        sites = response.body.split("\n")
        count = response.meta['count']
        max_page=response.meta['max_page']
        min_pin_id = 0
        board_id = 0
        for site in sites:
            site = site.strip().strip(';')
            if site.startswith('app.page["board"]'):
                json_str = site.split('=', 1)[-1]
                pint_items = json.loads(json_str)
                category_id=pint_items['category_id']
                category_name=pint_items['category_name']
                image_desc=pint_items['description']
                title=pint_items['title']
                for pin_item in pint_items['pins']:
                    item = MmSpiderItem()
                    item['board_id'] = pin_item['board_id']
                    item['category_id'] = category_id
                    item['file_id'] = pin_item['file_id']
                    item['image_url'] = img_host + pin_item['file']['key']
                    item['category_name'] =category_name
                    item['image_desc'] =image_desc
                    item['title'] =title
                    item['created_at']=pin_item['created_at']
                    if min_pin_id == 0 or min_pin_id > pin_item['pin_id']:
                        min_pin_id = pin_item['pin_id']
                    board_id = pin_item['board_id']
                    yield item
        count += 1
        if count == max_page:
            return
        if min_pin_id and board_id:
            next_url = board_host.format(board_id, min_pin_id)
            yield Request(next_url, meta={"count": count,"max_page":max_page}, callback=self.parse_board)

