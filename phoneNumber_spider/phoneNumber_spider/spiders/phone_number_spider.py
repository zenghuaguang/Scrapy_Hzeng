#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2016/9/2"
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

from scrapy import Spider, Selector, Request

from phoneNumber_spider.items import PhoneumberSpiderItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


class PhoneNumberSpider(Spider):
    name = "phoneSpider"
    allowed_domains = ["diaosiso.com"]
    start_urls = [
        "http://www.diaosiso.com/mobile_number/"
    ]
    download_delay = 1

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@class="container"]')
        count=0
        temp_capital=""
        for site in sites:
            # if count>4:
            #     break
            capital=site.xpath('h4/button/text()').extract()
            if capital:
                temp_capital=capital[0].strip().split(' ')[0]
            city_name = site.xpath('ul/li/a/text()').extract()
            url = site.xpath('ul/li/a/@href').extract()
            if len(city_name) > 0 and len(url) > 0:
                for i, city in enumerate(city_name):
                    city_name = city
                    city_url = url[i]
                    yield Request(city_url, meta={'city_name': city_name,"city_url":city_url,"capital":temp_capital}, callback=self.phone_parse)
                count+=1

    def phone_parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@class="container"]')
        phone_item = PhoneumberSpiderItem()
        city_name = response.meta['city_name']
        city_url = response.meta['city_url']
        capital=response.meta['capital']
        print "=========", str(city_name),city_url
        temp_prefix_name=[]
        for site in sites:
            prefix_name=site.xpath('h4/button/text()').extract()
            if len(prefix_name)>0:
                temp_prefix_name=prefix_name
            prefix_list=site.xpath('ul/li/text()').extract()
            phone_item['city_name'] = city_name
            phone_item['capital']=capital
            phone_item['prefix_name'] = [t.encode('utf-8').strip() for t in temp_prefix_name]
            phone_item['prefix_list'] = [l.encode('utf-8').strip() for l in prefix_list]
            # phone_item['city_name']=str(city_name)
            if len(temp_prefix_name)>0 and len(prefix_list)>0:
                yield  phone_item
