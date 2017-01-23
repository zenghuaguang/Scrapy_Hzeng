# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_id=scrapy.Field()
    mtb_id = scrapy.Field()
    mtb_name = scrapy.Field()
    mtb_info = scrapy.Field()
    category_id = scrapy.Field()
    image_urls = scrapy.Field()
    image_path=scrapy.Field()
