# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import logging
import os
import sqlite3
from sys import path
from pymongo import MongoClient
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.exporters import BaseItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings

from taobao_spider.items import TaobaoCategoryItem, TaobaoProductItem
from taobao_spider.upload_qiniu import upload


class TaobaoMongoSpiderPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.huaban_db = settings['HUABAN_DB']
        self.huaban_col = settings['HUABAN_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.huaban_db]
        self.collection = db[self.huaban_col]

    def process_item(self, item, spider):
        self.collection.update({"file_id": str(item["file_id"])}, dict(item), True)


class TaobaoJsonSpiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('catagory.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, TaobaoCategoryItem):
            line = json.dumps(dict(item)) + '\n'
            # print line
            self.file.write(line.decode("unicode_escape"))
        return item


class TaobaoJsonSpiderPipeline2(object):
    def __init__(self):
        self.file = codecs.open('product.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, TaobaoProductItem):
            line = json.dumps(dict(item)) + '\n'
            # print line
            self.file.write(line.decode("unicode_escape"))
        return item


class Sqlite3Pipeline(object):
    logger = logging.getLogger()

    def __init__(self):
        self.sqlite_file = settings['SQLITE_FILE']
        self.category_table = settings['SQLITE_TABLE']
        self.product_table = settings['SQLITE_TABLE2']
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        keys = item.fields.keys()
        value_str = ""
        for key in keys:
            if key in item.__dict__['_values']:
                value_str += '"' + item.__dict__['_values'][key] + '"' + ","
            else:
                keys.remove(key)
        value_str = value_str.strip(',')
        if isinstance(item, TaobaoProductItem):
            insert_sql = "insert into {0}({1}) values ({2})".format(self.product_table,
                                                                    ', '.join(keys),
                                                                    value_str)
        else:
            insert_sql = "insert into {0}({1}) values ({2})".format(self.category_table,
                                                                    ', '.join(keys),
                                                                    value_str)
        try:
            self.cur.execute(insert_sql)
            self.conn.commit()
        except Exception, e:
            self.logger.warn(e)
            self.logger.warn("出现错误...")

        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        upload("image/" + image_paths[0], image_paths[0])
        item['image_path'] = image_paths[0]
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}/{2}'.format(item['category_id'], item['board_id'], item['file_id']) + ".jpg"
        return filename
