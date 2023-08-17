# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class MongoDBConnectorPipeline(object):
    def __init__(self, mongo_uri, db_name: str, collection_name: str):
        '''
        mongo_uri is same as connection string: eg: mongodb://localhost:27017
        '''
        self.__mongo_uri = mongo_uri
        self.__db_name = db_name
        self.__collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("DB_NAME"),
            collection_name=crawler.settings.get("DB_COLLECTION_NAME")
        )

    def add_items_to_collection(self, item, spider):
        self.client = MongoClient(self.__mongo_uri)
        self.db = self.client[self.__db_name]
        self.db[self.__collection_name].insert_one(dict(item))
        self.client.close()
        return item
