from typing import Any

from bson import ObjectId

from main.domain.common.domain_mapper import DomainModelMapper, ValueObjectMapper
from main.domain.model.account_aggregate import Account, AccountType, Transaction
from main.domain.model.snapshot import Snapshot


class TransactionEntityMapper(ValueObjectMapper):

    def from_object(self, value_object: Transaction) -> dict:
        return {
            "date_created": value_object.date_created,
            "amount": value_object.amount
        }

    def to_object(self, entity: dict) -> Transaction:
        return Transaction(date_created=entity['date_created'],
                           amount=entity['amount'])


class SnapshotEntityMapper(ValueObjectMapper):

    def from_object(self, value_object: Snapshot) -> dict:
        return {
            "date": value_object.date,
            "amount": value_object.amount
        }

    def to_object(self, entity: Any) -> Snapshot:
        return Snapshot(date=entity['date'],
                        amount=entity['amount'])


class AccountEntityMapper(DomainModelMapper):

    def __init__(self):
        self.transaction_mapper = TransactionEntityMapper()
        self.snapshot_mapper = SnapshotEntityMapper()

    def from_domain_model(self, domain_model: Account) -> dict:
        return {
            '_id': ObjectId() if domain_model.id == "" else ObjectId(domain_model.id),
            'name': domain_model.name,
            'account_type': domain_model.account_type.value,
            'transactions': [self.transaction_mapper.from_object(transaction)
                             for transaction in domain_model.transactions],
            'snapshots': [self.snapshot_mapper.from_object(snapshot) for snapshot in domain_model.snapshots]
        }

    def to_domain_model(self, dbo: dict) -> Account:
        return Account(account_id=dbo['_id'],
                       name=dbo['name'],
                       account_type=AccountType[dbo['account_type']],
                       transactions=[self.transaction_mapper.to_object(transactionDbo)
                                     for transactionDbo in dbo['transactions']],
                       snapshots=[self.snapshot_mapper.to_object(snapshotDbo) for snapshotDbo in dbo['snapshots']])


