from dataclasses import dataclass
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

@dataclass(frozen=True)
class TransactionDto(Dto):
    date_created: str
    amount: float


@dataclass(frozen=True)
class SnapshotDto(Dto):
    timestamp: str
    amount: float


@dataclass(frozen=True)
class AccountDto(Dto):
    id: str
    name: str
    account_type: str
    transactions: List[TransactionDto]
    snapshots: List[SnapshotDto]


@dataclass(frozen=True)
class UserDto(Dto):
    id: str
    name: str
    email: str
    accounts: List[AccountDto]
    goals: List[SnapshotDto]


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


class UserDtoMapper(DomainModelMapper):
    account_mapper = AccountDtoMapper()
    snapshot_mapper = SnapshotDtoMapper()

    def from_domain_model(self, user: User) -> UserDto:
        return UserDto(id=user.id,
                       name=user.name,
                       email=user.email,
                       accounts=[self.account_mapper.from_domain_model(acc) for acc in user.accounts],
                       goals=[self.snapshot_mapper.from_object(goal) for goal in user.goals])
