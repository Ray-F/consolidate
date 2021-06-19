from pymongo import MongoClient


class MongoService:

    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.database = self.client[db_name]

        print("[Server] Mongo service initiated")
