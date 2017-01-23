# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()
    host = scrapy.Field()
    port = scrapy.Field()
    location = scrapy.Field()
    anonymity = scrapy.Field()
    type = scrapy.Field()
    speed = scrapy.Field()
    connect_time = scrapy.Field()
    survive_time = scrapy.Field()
    verify_time = scrapy.Field()
    update_time = scrapy.Field()
