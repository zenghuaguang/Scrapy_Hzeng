# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib

from pymongo import MongoClient
from scrapy.conf import settings


def item_format(item):
    for k, v in item.items():
        if k=="update_time":
            continue
        v_temp = ""
        for v_item in v:
            v_item = v_item.strip()
            if "://" not in v_item:
                v_temp += v_item
        if v_temp:
            item[k] = v_item
    return item

class MongoQbImagePipeline(object):
    url="http://ip.chinaz.com/getip.aspx"
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        item=item_format(item)
        self.collection.update({"host": str(item["host"])}, dict(item), True)

