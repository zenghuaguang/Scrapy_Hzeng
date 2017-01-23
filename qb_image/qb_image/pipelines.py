# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import base64
import codecs
import json
import urllib2

import bson
import requests
from pymongo import MongoClient
from scrapy.conf import settings


def item_format(item):
    for k, v in item.items():
        if k == "comments":
            continue
        v_temp = ""
        for v_item in v:
            v_item = v_item.strip()
            if "://" not in v_item:
                v_temp += v_item
        if v_temp:
            item[k] = v_item
    return item


class QbImagePipeline(object):
    def __init__(self):
        self.file = codecs.open('qb.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        item = item_format(item)
        line = json.dumps(dict(item)) + '\n'
        # print line
        self.file.write(line.decode("unicode_escape"))
        return item


class MongoQbImagePipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        data=None
        for img_url in item['user_image']:
            response = urllib2.urlopen(img_url)
            data = response.read()
            data = base64.b64encode(data)
        if data:
            item['user_image'] = bson.binary.Binary(data)
        data=None
        for img_url in item['content_image']:
            response = urllib2.urlopen(img_url)
            data = response.read()
            response.close()
            data = base64.b64encode(data)
        if data:
            item['content_image'] = bson.binary.Binary(data)
        self.collection.update({"article_id": str(item["article_id"])}, dict(item), True)
