# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongoDBPipeline(object):
    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get("MONGODB_URI", "mongodb://localhost:27017"),
            mongodb_db=crawler.settings.get("MONGODB_DATABASE", "crawler"),
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        :param item: 传入的item数据
        :param spider: spider相关信息
        :return item:
        """
        if item.get("code"):
            self.db[str(spider.name).split("_")[0].lower()].update_one(
                filter={"code": item["code"]}, update={"$set": dict(item)}, upsert=True
            )
        return item
