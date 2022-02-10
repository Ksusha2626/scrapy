import json

from bson.json_util import dumps

from pymongo import MongoClient

from leroyparser.spiders.leroymerlin import LeroymerlinSpider
from leroyparser.pipelines import MONGODB


def save_json(data):
    with open('file_output.json', 'w') as f:
        json.dump(json.loads(dumps(data)), f, indent=2, ensure_ascii=False)


def save_leroymerlin(client):
    db = client[LeroymerlinSpider.name]
    collection = db['kuhonnye-moyki']
    save_json(collection.find({}))


if __name__ == '__main__':
    mongodb = MongoClient(MONGODB)
    save_leroymerlin(mongodb)
