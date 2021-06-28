import os
import unittest
from datetime import datetime

from main.domain.model.account_aggregate import Transaction, Account, AccountType
from main.domain.model.snapshot import Snapshot
from main.domain.model.user import User
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository
from main.infrastructure.repository.user_repository import UserRepository


class UserRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.__mongo_service = MongoService(os.environ.get("MONGO_URI"), "consolidate-dev")
        self.__account_repo = AccountRepository(mongo_service=self.__mongo_service)
        self.__user_repo = UserRepository(mongo_service=self.__mongo_service, account_repo=self.__account_repo)

    @unittest.skip
    def test_action_addAnAccount(self):
        transaction1 = Transaction(date_created=datetime.now(), amount=10_000)
        latest_snapshot = Snapshot(timestamp=datetime.now(), amount=9_500)
        transaction2 = Transaction(date_created=datetime.now(), amount=6_500)

        account = Account(id="",
                          name="Kiwisaver",
                          account_type=AccountType.SIMPLICITY,
                          transactions=[transaction1, transaction2],
                          snapshots=[latest_snapshot])

        self.__account_repo.save(account)

    def test_addNewUser(self):
        account = self.__account_repo.get_account_by_id(id="60cf3c704036bd990e90430c")

        goals = [Snapshot(timestamp=datetime(2021, 12, 30), amount=1_000),
                 Snapshot(timestamp=datetime(2022, 6, 30), amount=2_000)]

        new_user = User(id="60d04c24edd16a7f2e814202",
                        name="Raymond Feng",
                        email="rf.raymondfeng@gmail.com",
                        profile_picture="https://www.rayf.me/static/media/profile_picture.4452a610.jpg",
                        accounts=[account],
                        goals=goals)

        self.__user_repo.save(new_user)

    def test_addSecondUser(self):
        # Simplicity account
        account1 = self.__account_repo.get_account_by_id("60cf3c92efed09873d5dea0c")

        # KiwiSaver account
        account2 = self.__account_repo.get_account_by_id("60cf460a32c20609b6ef3223")
        account2.transactions[0].amount = 20

        new_user = User(id="60d05277a7fb635c9969165e",
                        name="John Snow",
                        email="jon@thoughtworks.com",
                        profile_picture="",
                        accounts=[account1, account2],
                        goals=[])

        self.__user_repo.save(new_user)

    @unittest.skip("enable when clearing DB")
    def test_deleteAllUsers(self):
        self.__mongo_service.collection("users").delete_many({})
