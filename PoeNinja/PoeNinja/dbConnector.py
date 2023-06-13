import pymongo


class DBConnector:
    def __init__(self, client_path: str, db_name: str, collection_name: str):
        """
        connection string: eg: mongodb://localhost:27017
        """
        self.__client_path = client_path
        self.__db_name = db_name
        self.__collection_name = collection_name

    def make_collection(self):
        """
        :return: collection
        """
        client = pymongo.MongoClient(self.__client_path)
        db = client[self.__db_name]
        return db[self.__collection_name]

    def get_client_path(self):
        """
        same as db connection string
        """
        return self.__client_path

    def get_db_name(self):
        return self.__db_name

    def get_collection_name(self):
        return self.__collection_name

    def count_documents(self):
        """
        returns the number of documents in the collection
        """
        return self.make_collection().count_documents({})

    def to_string(self):
        return f"connection string or client path: {self.__client_path}\n\
                database name: {self.__db_name}\n\
                collection name: {self.__collection_name}\n\
                documents: {self.count_documents()}"
