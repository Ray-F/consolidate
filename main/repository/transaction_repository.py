from bson import ObjectId

from main.domain.model.transaction import Transaction
from main.domain.util.domain_mapper import DomainModelMapper
from main.service.mongo_service import MongoService


class TransactionEntityMapper(DomainModelMapper):

    def from_domain_model(self, domain_model: Transaction) -> dict:
        return {
            "_id": ObjectId() if domain_model.id == "" else ObjectId(domain_model.id),
            "account_id": ObjectId(domain_model.account_id),
            "date_created": domain_model.date_created,
            "amount": domain_model.amount
        }

    def to_domain_model(self, entity: dict) -> Transaction:
        return Transaction(transaction_id=str(entity['_id']),
                           account_id=str(entity['account_id']),
                           date_created=entity['date_created'],
                           amount=entity['amount'])


class TransactionRepository:

    entityMapper = TransactionEntityMapper()

    def __init__(self, mongo_service: MongoService):
        self.__transactions_collection = mongo_service.collection("transactions")

    def get_all_transactions(self):
        """
        Returns all transactions in the collection.
        :return:
        """

        return [
            self.entityMapper.to_domain_model(dbo)
            for dbo in self.__transactions_collection.find({})
        ]

    def add_transaction(self, transaction: Transaction) -> Transaction:
        """
        Adds a transaction to the database.
        :return: The transaction that was added.
        """

        dbo = self.entityMapper.from_domain_model(transaction)

        result = self.__transactions_collection.insert_one(dbo).inserted_id

        return self.entityMapper.to_domain_model(dbo)
