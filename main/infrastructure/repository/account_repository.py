from typing import List

from bson import ObjectId

from main.domain.common.repository import Repository
from main.domain.model.account_aggregate import Account
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.entity_mapper import AccountEntityMapper


class AccountRepository(Repository):

    def __init__(self, mongo_service: MongoService):
        self.__account_collection = mongo_service.collection("accounts")
        self.__account_mapper = AccountEntityMapper()

    def list(self) -> List[Account]:
        dbo_list = self.__account_collection.find({})
        return [self.__account_mapper.to_domain_model(dbo) for dbo in dbo_list]

    def save(self, account: Account) -> Account:
        dbo = self.__account_mapper.from_domain_model(account)

        if account.id:
            self.__account_collection.update_one({'_id': ObjectId(account.id)}, {'$set': dbo}, upsert=True)
            return account
        else:
            self.__account_collection.insert_one(dbo)
            return self.__account_mapper.to_domain_model(dbo)

    def get_account_by_id(self, id: str):
        """
        Gets the account by the associated ID and returns it.

        :param id: The id of the account.
        :return: The account.
        """

        dbo = self.__account_collection.find_one({'_id': ObjectId(id)})
        return self.__account_mapper.to_domain_model(dbo)
