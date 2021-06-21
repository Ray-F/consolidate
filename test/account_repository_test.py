import os
import unittest
from datetime import datetime

from main.domain.model.account_aggregate import Transaction, Account, AccountType
from main.domain.model.snapshot import Snapshot
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository


class AccountRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.__account_repo = AccountRepository(mongo_service=MongoService(os.environ.get("MONGO_URI"),
                                                                           "consolidate-dev"))

    def test_action_addAnAccount(self):
        """
        Adds another account to our database.

        :return:
        """
        transaction = Transaction(date_created=datetime.now(), amount=10_000)
        latest_snapshot = Snapshot(date=datetime.now(), amount=9_500)
        transaction2 = Transaction(date_created=datetime.now(), amount=6_500)

        account = Account(account_id="",
                          name="Kiwisaver",
                          account_type=AccountType.SIMPLICITY,
                          transactions=[transaction, transaction2],
                          snapshots=[latest_snapshot])

        self.__account_repo.add(account)
