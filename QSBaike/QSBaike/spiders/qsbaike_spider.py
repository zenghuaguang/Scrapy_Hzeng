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
from scrapy import Spider, Selector, Request
from QSBaike.items import QsbaikeItem

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')


class QSBaiKeSpider(Spider):
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "qsbaike"
    allowed_domains = ["qiushibaike.com"]
    start_urls = [
        "http://www.qiushibaike.com/text/"
    ]
    download_delay = 1
    count = 0

    def parse(self, response):
        host="http://www.qiushibaike.com"
        sel = Selector(response)
        sites = sel.xpath('//*[@id="content-left"]/div')
        for site in sites:
            item = QsbaikeItem()
            article_id = site.xpath('a[@class="contentHerf"]/@href').extract()
            #div/a/img
            use_name = site.xpath('div/a/h2/text()').extract()
            user_image= site.xpath('div/a/img/@src').extract()
            content = site.xpath('a[@class="contentHerf"]/div/span/text()').extract()
            item['article_id'] = [t.encode('utf-8').split('/')[-1] for t in article_id]
            item['user_name'] = [t.encode('utf-8') for t in use_name]
            item['user_image'] = user_image
            item['content'] = [l.encode('utf-8').strip() for l in content]
            comments_url=site.xpath('div/span/a[@class="qiushi_comments"]/@href').extract()
            if comments_url:
               yield Request(host+comments_url[0],meta={"item" : item},callback=self.parse_comments)
            else:
                yield item
        self.count += 1
        if self.count == 500:
            return
        urls = sel.xpath('//*[@id="content-left"]/ul/li/a[@rel="nofollow"]/@href').extract()
        url = host + urls[-1]
        yield Request(url, callback=self.parse)


    def parse_comments(self, response):
        item = response.meta['item']

        sel = Selector(response)
        #godCmt > div > div
        sites = sel.xpath('//*[@id="godCmt"]/div/div[@class="comments-list-item"]/div[@class="comments-table"]')
        comments_dict={}
        for site in sites:
            comments_user=site.xpath('a/div[@class="main-name"]/div[@class="cmt-name"]/text()').extract()
            comments_text=site.xpath('a/div[@class="main-text"]/text()').extract()
            comments_dict[comments_user[0].strip().strip('\n')]=comments_text[0].strip().strip('\n')
        item['comments']=comments_dict
        yield  item


