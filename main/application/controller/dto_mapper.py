from typing import List

from main.domain.common.domain_mapper import DomainModelMapper, ValueObjectMapper
from main.domain.common.entities import Dto, DomainModel
from main.domain.model.account_aggregate import Account, AccountType, Transaction
from main.domain.model.snapshot import Snapshot
from main.domain.model.user import User
from main.util.localdatetime import parse_isostring_with_tz


# TODO: Rethink the whole structure around DTO mapping, since we could have many different types of DTO for different
#  purposes (such as a partial DTO instead of a full object DTO).
#  Further, we should have some application services that call methods to retrieve the larger domain models if we need
#  more attributes, so we should consider just passing the ones needed for certain endpoint functionalities.

class TransactionDto(Dto):

    def __init__(self, date_created: str, amount: float):
        self.date_created: str = date_created
        self.amount: float = amount


class SnapshotDto(Dto):

    def __init__(self, timestamp: str, amount: float):
        self.timestamp = timestamp
        self.amount = amount


class AccountDto(Dto):

    def __init__(self,
                 id: str,
                 name: str,
                 account_type: str,
                 transactions: List[TransactionDto],
                 snapshots: List[SnapshotDto]):
        self.id = id
        self.name = name
        self.account_type = account_type
        self.transactions = transactions
        self.snapshots = snapshots


class SnapshotDtoMapper(ValueObjectMapper):
    def from_object(self, snapshot: Snapshot) -> SnapshotDto:
        return SnapshotDto(timestamp=snapshot.timestamp.isoformat(), amount=snapshot.amount)

    def to_object(self, model: SnapshotDto) -> Snapshot:
        return Snapshot(timestamp=parse_isostring_with_tz(model.timestamp), amount=model.amount)


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
        return Account(id=model.id,
                       name=model.name,
                       account_type=AccountType[model.account_type],
                       transactions=[self.transaction_mapper.to_object(dto) for dto in model.transactions],
                       snapshots=[self.snapshot_mapper.to_object(dto) for dto in model.snapshots])


class UserDto(Dto):
    account_mapper = AccountDtoMapper()
    snapshot_mapper = SnapshotDtoMapper()

    def __init__(self, id: str, name: str, email: str, accounts: List[AccountDto], goals: List[SnapshotDto]):
        self.id = id
        self.name = name
        self.email = email
        self.accounts = accounts
        self.goals = goals

    # FIXME: Temporary method for displaying a DTO on screen.
    @classmethod
    def to_dto(cls, user: User):
        return UserDto(id=user.id,
                       name=user.name,
                       email=user.email,
                       accounts=[cls.account_mapper.from_domain_model(acc) for acc in user.accounts],
                       goals=[cls.snapshot_mapper.from_object(goal) for goal in user.goals])
