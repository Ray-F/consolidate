from pymongo import MongoClient
from pymongo.collection import Collection


class MongoService:

    def __init__(self, uri, db_name):
        self.__client = MongoClient(uri)
        self.__database = self.__client[db_name]

        print("[Server] Mongo service initiated")

    def collection(self, collection_name: str) -> Collection:
        return self.__database[collection_name]
