# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pprint import pprint

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

MONGODB = '127.0.0.1:27017'


class LeroyparserPipeline:
    def __init__(self):
        self.mongodb = MongoClient(MONGODB)

    def process_item(self, item, spider):
        self.update_db(spider, item)
        pprint(item)
        return item

    def update_db(self, spider, data):
        db = self.mongodb[f'{spider.name}']
        collection = db[spider.category]
        if 'index' not in collection.index_information():
            collection.create_index('url', name='index', unique=True)
        collection.replace_one({'url': data['url']}, data, upsert=True)
        # pprint(data)
        # pprint(collection.count_documents({}))
        # for item in collection.find({}):
        #     pprint(item)
        # collection.drop()
        # self.mongodb.drop_database(db.name)


class LeroyparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
