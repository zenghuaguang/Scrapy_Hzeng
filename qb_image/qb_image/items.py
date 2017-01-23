# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QbImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    user_image = scrapy.Field()
    content_image = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    comments = scrapy.Field()


class HbImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pin_id = scrapy.Field()
    image_url = scrapy.Field()
