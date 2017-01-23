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
from moko_spider.items import MmSpiderItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


class HbImageSpider(Spider):
    logger = logging.getLogger()
    """爬取moko标签"""
    # log.start("log",loglevel='INFO')
    name = "moko_boards"
    allowed_domains = ["www.moko.cc"]
    start_urls = [
        "http://www.moko.cc/mtb.html"
    ]

    def parse(self, response):
        host = "http://www.moko.cc"
        sel = Selector(response)
        sites = sel.xpath('//*[@id="mspshow"]/div')
        for site in sites:
            board_count = 0
            category_id=site.xpath("@id").extract()[0]
            sub_sites = site.xpath('dl/dd/a/@href').extract()
            for sub_site in sub_sites:
                board_url = host + sub_site
                if board_count == 20:
                    break
                yield Request(board_url, meta={"category_id":category_id}, callback=self.parse_board)
                board_count += 1

    def parse_board(self, response):
        self.logger.info('url:{0}'.format(response.url))
        sel = Selector(response)
        info_sites = sel.xpath('//*[@id="form_profile"]/ul/li')
        image_sites = sel.xpath('//*[@id="div_thumbnail_box"]/dl/dd')
        mtb_name = sel.xpath('//*[@id="spaceHeader"]/div[1]/a/text()').extract()[0]
        item=MmSpiderItem()
        mtb_id=response.url.split('/')[-2]
        category_id=response.meta['category_id']
        item['mtb_name']=mtb_name
        item['mtb_id']=mtb_id
        item['category_id']=category_id
        info={}
        for site in info_sites:
            key = site.xpath('span/text()').extract()[0]
            vaule = site.xpath('input/@value').extract()[0]
            info[key]=vaule
        item['mtb_info']=info
        img_urls=[]
        for site in image_sites:
            img_url = site.xpath('img/@src').extract()[0]
            img_url = img_url.split("?")[0]
            self.logger.info(img_url)
            img_urls.append(img_url)
        item['image_urls']=img_urls
        yield item
