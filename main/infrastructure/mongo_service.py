from pymongo import MongoClient
from pymongo.collection import Collection


class MongoService:
    """
    Wrapper for interacting with MongoDB.
    """

    def __init__(self, uri, db_name):
        """
        Connecting to a Mongo Atlas cluster.

        :param uri: Mongo atlas uri with credentials.
        :param db_name: The name of the database to connect to.
        """
        self.__client = MongoClient(uri, ssl=True, tlsAllowInvalidCertificates=True)
        self.__database = self.__client[db_name]

        print("[Server] Mongo service initiated")

    def collection(self, collection_name: str) -> Collection:
        return self.__database[collection_name]
