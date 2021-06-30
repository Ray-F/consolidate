from bson import ObjectId

from main.domain.common.domain_mapper import DomainModelMapper, ValueObjectMapper
from main.domain.model.account_aggregate import Account, AccountType, Transaction
from main.domain.model.snapshot import Snapshot
from main.domain.model.user import User


class TransactionEntityMapper(ValueObjectMapper):

    def from_object(self, value_object: Transaction) -> dict:
        return {
            "date_created": value_object.date_created,
            "amount": value_object.amount
        }

    def to_object(self, entity: dict) -> Transaction:
        return Transaction(date_created=entity['date_created'], amount=entity['amount'])


class SnapshotEntityMapper(ValueObjectMapper):

    def from_object(self, value_object: Snapshot) -> dict:
        return {
            "datetime": value_object.timestamp,
            "amount": value_object.amount
        }

    def to_object(self, entity: dict) -> Snapshot:
        return Snapshot(timestamp=entity['datetime'], amount=entity['amount'])


class AccountEntityMapper(DomainModelMapper):

    def __init__(self):
        self.transaction_mapper = TransactionEntityMapper()
        self.snapshot_mapper = SnapshotEntityMapper()

    def from_domain_model(self, domain_model: Account) -> dict:
        return {
            '_id': ObjectId() if (domain_model.id == "" or domain_model.id is None) else ObjectId(domain_model.id),
            'name': domain_model.name,
            'account_type': domain_model.account_type.name,
            'transactions': [self.transaction_mapper.from_object(transaction)
                             for transaction in domain_model.transactions],
            'snapshots': [self.snapshot_mapper.from_object(snapshot) for snapshot in domain_model.snapshots]
        }

    def to_domain_model(self, dbo: dict) -> Account:
        return Account(id=str(dbo['_id']),
                       name=dbo['name'],
                       account_type=AccountType[dbo['account_type']],
                       transactions=[self.transaction_mapper.to_object(transaction_dbo)
                                     for transaction_dbo in dbo['transactions']],
                       snapshots=[self.snapshot_mapper.to_object(snapshot_dbo) for snapshot_dbo in dbo['snapshots']])


class UserEntityMapper(DomainModelMapper):

    def __init__(self):
        self.__snapshot_mapper = SnapshotEntityMapper()
        self.__account_mapper = AccountEntityMapper()

    def from_domain_model(self, domain_model: User) -> dict:
        return {
            '_id': ObjectId() if (domain_model.id == "" or domain_model.id is None) else ObjectId(domain_model.id),
            'name': domain_model.name,
            'email': domain_model.email,
            'account_ids': [ObjectId(account.id) for account in domain_model.accounts],
            'profile_picture': domain_model.profile_picture,
            'goals': [self.__snapshot_mapper.from_object(goal) for goal in domain_model.goals],
        }

    def to_domain_model(self, dbo: dict) -> User:
        return User(id=str(dbo['_id']),
                    name=dbo['name'],
                    email=dbo['email'],
                    profile_picture=dbo['profile_picture'],
                    accounts=[self.__account_mapper.to_domain_model(account_dbo) for account_dbo in dbo['accounts']],
                    goals=[self.__snapshot_mapper.to_object(goal_dbo) for goal_dbo in dbo['goals']])
