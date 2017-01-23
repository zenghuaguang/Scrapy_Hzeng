# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
from moko_spider.upload_qiniu import upload_without_key, upload


class MmSpiderPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.huaban_db = settings['HUABAN_DB']
        self.huaban_col = settings['HUABAN_COLLECTION']
        connection = MongoClient(self.server, self.port)
        db = connection[self.huaban_db]
        self.collection = db[self.huaban_col]
    def process_item(self, item, spider):
        self.collection.update({"mtb_id": str(item["mtb_id"])}, dict(item), True)


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        for image_path in image_paths:
            upload("image/" + image_path, image_path)
        item['image_path'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}/{2}'.format(item['category_id'], item['mtb_id'], image_guid)
        return filename
