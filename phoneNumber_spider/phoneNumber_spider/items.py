# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhoneumberSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    capital=scrapy.Field()
    city_name=scrapy.Field()
    prefix_name=scrapy.Field()
    prefix_list=scrapy.Field()
    city_url=scrapy.Field()
