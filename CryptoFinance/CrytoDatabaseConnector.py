from pymongo import MongoClient


class DBConnector:
    collection_name = ""
    """
    connection string: eg: mongodb://localhost:27017\n
    db_name: String - database name\n
    collection_name: String - collection name where documents are stored
    """

    def __init__(self, connection_string: str, db_name: str):
        self.__connection_string = connection_string
        self.__db_name = db_name
        client = MongoClient(self.__connection_string)
        self.db = client[self.__db_name]

    def create_collection(self, collection_name):
        return self.db[collection_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
