# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class PoeNinjaDBPipeline:

    def __init__(self, client_path: str="mongodb://localhost:27017/",
                 db_name: str="poe_ninja",
                 collection_name: str="divine_orb1"):
        """
        client path is same as connection string: eg: mongodb://localhost:27017
        """
        self.__client_path = client_path
        self.__db_name = db_name
        self.__collection_name = collection_name

    def open_spider(self, spider):
        self.client = MongoClient(self.__client_path)
        self.db = self.client[self.__db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.__collection_name].insert_one(dict(item))
        return item
