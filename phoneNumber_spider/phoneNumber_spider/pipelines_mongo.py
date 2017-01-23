# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from phoneNumber_spider import settings


class PhoneNumberPipeline(object):
   def __init__(self, pymongo=None):
        connection = pymongo.Connection(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

   def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        # print line
        self.file.write(line.decode("unicode_escape"))
        return item
