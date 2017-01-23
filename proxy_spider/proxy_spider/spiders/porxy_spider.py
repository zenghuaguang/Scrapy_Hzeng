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
import sys
import datetime
import urllib
from scrapy import Spider, Selector, Request
from scrapy.crawler import CrawlerProcess

from proxy_spider.items import ProxySpiderItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


class ProxySpider(Spider):
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "proxy_spider"
    allowed_domains = ["www.xicidaili.com"]
    start_urls = [
        "http://www.xicidaili.com/nn/"
    ]
    count = 0

    def parse(self, response):
        host = "http://www.xicidaili.com/nn/"
        sel = Selector(response)
        sites = sel.xpath('//*[@id="body"]/table/tr')
        for site in sites:
            item = ProxySpiderItem()
            sub_sites = site.xpath('td')
            if sub_sites:
                item['country'] = sub_sites[0].xpath('img/@alt').extract()
                item['host'] = sub_sites[1].xpath('text()').extract()
                item['port'] = sub_sites[2].xpath('text()').extract()
                item['location'] = sub_sites[3].xpath('a/text()').extract()
                item['anonymity'] = sub_sites[4].xpath('text()').extract()
                item['type'] = sub_sites[5].xpath('text()').extract()
                item['speed'] = sub_sites[6].xpath('div/@title').extract()
                item['connect_time'] = sub_sites[7].xpath('div/@title').extract()
                item['survive_time'] = sub_sites[8].xpath('text()').extract()
                item['verify_time'] = sub_sites[9].xpath('text()').extract()
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield item
        self.count += 1
        if self.count == 2:
            return
        url = host + str(self.count)
        yield Request(url, callback=self.parse)


