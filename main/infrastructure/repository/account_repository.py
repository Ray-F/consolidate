import os
import unittest
from datetime import datetime
from typing import List

from main.domain.model.account_aggregate import Account, AccountType, Transaction, Snapshot
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.entity_mapper import AccountEntityMapper


class AccountRepository:

    def __init__(self, mongo_service: MongoService):
        self.__account_collection = mongo_service.collection("accounts")
        self.__account_mapper = AccountEntityMapper()

    def list(self) -> List[Account]:
        """
        Gets a list of all `Account`'s stored in the collection and returns them.

        :return: List of accounts
        """
        return [
            self.__account_mapper.to_domain_model(dbo)
            for dbo in self.__account_collection.find({})
        ]

    def add(self, account: Account) -> Account:
        """
        Adds an `Account` to the collection.

        :param account: The account to add.
        :return:
        """
        dbo = self.__account_mapper.from_domain_model(account)

        result = self.__account_collection.insert_one(dbo).inserted_id

        return self.__account_mapper.to_domain_model(dbo)