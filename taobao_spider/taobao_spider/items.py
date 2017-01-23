# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoCategoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    parent_id = scrapy.Field()

class TaobaoProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_id = scrapy.Field()
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_title = scrapy.Field()
    product_price = scrapy.Field()
    product_img = scrapy.Field()
    product_sum = scrapy.Field()
    product_link = scrapy.Field()