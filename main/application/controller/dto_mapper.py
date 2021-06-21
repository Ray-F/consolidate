from typing import List

from main.domain.model.account_aggregate import Account, AccountType, Transaction
from main.domain.common.domain_mapper import DomainModelMapper, ValueObjectMapper
from main.domain.common.entities import Dto, DomainModel
from main.domain.model.snapshot import Snapshot
from main.util.localdatetime import parse_isostring_with_tz


class TransactionDto(Dto):

    def __init__(self, date_created: str, amount: float):
        super().__init__()

        self.date_created: str = date_created
        self.amount: float = amount


class SnapshotDto(Dto):

    def __init__(self, date: str, amount: float):
        super().__init__()

        self.date = date
        self.amount = amount


class AccountDto(Dto):

    def __init__(self,
                 id: str,
                 name: str,
                 account_type: str,
                 transactions: List[TransactionDto],
                 snapshots: List[SnapshotDto]):
        super().__init__()

        self.id = id
        self.name = name
        self.account_type = account_type
        self.transactions = transactions
        self.snapshots = snapshots


class SnapshotDtoMapper(ValueObjectMapper):
    def from_object(self, snapshot: Snapshot) -> SnapshotDto:
        return SnapshotDto(date=snapshot.date.isoformat(), amount=snapshot.amount)

    def to_object(self, model: SnapshotDto) -> Snapshot:
        return Snapshot(date=parse_isostring_with_tz(model.date), amount=model.amount)


class TransactionDtoMapper(ValueObjectMapper):
    def from_object(self, transaction: Transaction) -> TransactionDto:
        return TransactionDto(date_created=transaction.date_created.isoformat(),
                              amount=transaction.amount)

    def to_object(self, model: TransactionDto) -> Transaction:
        return Transaction(date_created=parse_isostring_with_tz(model.date_created),
                           amount=model.amount)


class AccountDtoMapper(DomainModelMapper):
    snapshot_mapper = SnapshotDtoMapper()
    transaction_mapper = TransactionDtoMapper()

    def from_domain_model(self, account: Account) -> AccountDto:
        transactions = [self.transaction_mapper.from_object(transaction) for transaction in account.transactions]
        snapshots = [self.snapshot_mapper.from_object(model) for model in account.snapshots]

        return AccountDto(id=str(account.id),
                          name=account.name,
                          account_type=account.account_type.value,
                          transactions=transactions,
                          snapshots=snapshots)

    def to_domain_model(self, model: AccountDto) -> DomainModel:
        return Account(account_id=model.id,
                       name=model.name,
                       account_type=AccountType[model.account_type],
                       transactions=[self.transaction_mapper.to_object(dto) for dto in model.transactions],
                       snapshots=[self.snapshot_mapper.to_object(dto) for dto in model.snapshots])
