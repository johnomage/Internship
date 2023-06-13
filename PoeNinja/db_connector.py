import datetime

import pymongo


class DBConnector:
    def __init__(self, client_path: str, db_name: str, collection_name: str):
        self.client_path = client_path
        self.db_name = db_name
        self.collection_name = collection_name

    def connect_to_db(self):
        client = pymongo.MongoClient(self.client_path)
        db = client[self.db_name]
        collection = db[self.collection_name]
        return collection


