# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pprint import pprint

from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongobase = self.client.jobs

    def process_item(self, item, spider):
        salary = self.process_salary(item.get('salary'), spider)
        item['min_salary'], item['max_salary'], item['cur'] = salary
        self.update_db(spider, item)
        pprint(item)
        return item

    @staticmethod
    def process_salary(data, spider):
        min_salary, max_salary, cur = None, None, None
        data = [x.replace('\u202f', '').replace(u'\xa0', '') for x in data if x != ' ']
        for i, v in enumerate(data):
            if v.strip() == 'от':
                min_salary = int(data[i + 1].replace('руб.', ''))
            if v.strip() == 'до':
                max_salary = int(data[i + 1].replace('руб.', ''))
        if spider.name == 'hhru':
            if len(data) > 1:
                cur = data[-2]
        if spider.name == 'superjob':
            if 'от' not in data and 'до' not in data and len(data) > 1:
                if len(data) == 3:
                    min_salary = int(data[0])
                    cur = data[-2]
                else:
                    min_salary = int(data[0])
                    max_salary = int(data[1])
                    cur = data[-2]
        return min_salary, max_salary, cur

    def update_db(self, spider, data):
        collection = self.mongobase[spider.name]
        if 'index' not in collection.index_information():
            collection.create_index('url', name='index', unique=True)
        pprint(data)
        pprint(collection.count_documents({}))

        collection.replace_one({'url': data['url']}, data, upsert=True)
        # for job in collection.find({}):
        #     pprint(job)
        # collection.drop()
        # self.client.drop_database('jobs')
