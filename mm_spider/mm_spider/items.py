# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    board_id=scrapy.Field()
    category_id=scrapy.Field()
    file_id = scrapy.Field()
    image_url = scrapy.Field()
    category_name=scrapy.Field()
    image_desc=scrapy.Field()
    created_at=scrapy.Field()
    title=scrapy.Field()
    image_path=scrapy.Field()