# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import base64
import codecs
import json
import bson
from pymongo import MongoClient
from scrapy import Request
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from QSBaike.settings import IMAGES_STORE


class QsbaikePipeline(object):
    def __init__(self):
        self.file = codecs.open('qb.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        for k, v in item.items():
            if k == "comments":
                continue
            temp = ''.join(v)
            item[k] = temp
        line = json.dumps(dict(item)) + '\n'
        # print line
        self.file.write(line.decode("unicode_escape"))
        return item


class MongoQsbaikePipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        for k, v in item.items():
            if k == "comments":
                continue
            temp = ''.join(v)
            item[k] = temp
        self.collection.update({"article_id": str(item["article_id"])}, dict(item), True)


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['user_image']
        yield Request(image_url)

    def item_completed(self, results, item, info):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        with open(IMAGES_STORE + image_paths[0], 'rb') as image_file:
            data = image_file.read()
            data=base64.b64encode(data)
            item['user_image'] = bson.binary.Binary(data)
        self.collection.update({"article_id": str(item["article_id"])}, dict(item), True)
        return item
