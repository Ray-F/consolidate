from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional

from main.domain.common.entities import DomainModel, ValueObject
from main.domain.common.errors import DomainError
from main.domain.model.snapshot import Snapshot, sort_snapshots
from main.util.localdatetime import LOCAL_TIMEZONE


class AccountType(Enum):
    """
    The type of account (either platform or asset type, i.e. Money) the account is.
    """

    ASB = auto(),
    BNZ = auto(),
    ANZ = auto(),

    SIMPLICITY = auto(),
    KIWISAVER = auto(),

    SHARESIES = auto(),
    HATCH = auto(),

    CASH = auto()


@dataclass(frozen=True)
class Transaction(ValueObject):
    """
    A real transaction made by the user into (or out of) an asset account.

    :param date_created: The date the transaction was made.
    :param amount: The amount of the transaction (positive or negative to 2 DP).
    """
    date_created: datetime
    amount: float


def sort_transactions(transactions_list: List[Transaction]) -> List[Transaction]:
    """
    Sorts a list of transactions in order of the most recent (index 0) to oldest (index -1).

    :param transactions_list: The list of transactions to sort.
    :return: A sorted list of transactions.
    """
    return sorted(transactions_list, key=lambda x: x.date_created, reverse=True)


class Account(DomainModel):

    def __init__(self,
                 id: str,
                 name: str,
                 creation_time: Optional[datetime],
                 account_type: AccountType,
                 transactions: List[Transaction],
                 snapshots: List[Snapshot]) -> None:
        """
        An asset account.

        :param id: A unique ID for all accounts (automatically generated).
        :param name: A human readable name (provided by the user) of the account.
        :param account_type: The account type.
        :param transactions: List of all transactions made for this account.
        :param snapshots: List of all account snapshots in the past.
        """
        self.id: str = id
        self.name: str = name
        self.account_type: AccountType = account_type
        self.transactions: List[Transaction] = transactions
        self.snapshots: List[Snapshot] = snapshots
        self.creation_time: datetime = creation_time or datetime.now(tz=LOCAL_TIMEZONE)

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def add_snapshot(self, snapshot: Snapshot):
        # Raise domain exception if the snapshot to be added to the account is in the future
        if snapshot.timestamp > datetime.now(tz=LOCAL_TIMEZONE):
            raise DomainError

        self.snapshots.append(snapshot)

    def get_expected_balance(self) -> float:
        """
        Returns the most accurate value for an account's existing asset value, based on the latest snapshot and then
        adding transactions that have happened since the snapshot was taken.

        :return: the expected balance amount.
        """

        # Sort the list of snapshots and take the most recent one
        latest_snapshot = self.get_most_recent_snapshot()

        latest_snapshot_amount = latest_snapshot.amount if latest_snapshot else 0
        latest_snapshot_timestamp = latest_snapshot.timestamp if latest_snapshot else self.creation_time

        # Get the sum of all transaction amounts between the latest snapshot (if it exists) and now
        def within_snap_and_now(trans: Transaction):
            return latest_snapshot_timestamp.astimezone(tz=LOCAL_TIMEZONE) \
                   < trans.date_created.astimezone(tz=LOCAL_TIMEZONE) \
                   < datetime.now(tz=LOCAL_TIMEZONE)

        transactions_sum = sum([t.amount for t in filter(within_snap_and_now, self.transactions)])

        return latest_snapshot_amount + transactions_sum

    def get_recent_snapshots(self, limit: int) -> List[Snapshot]:
        """
        Returns a list of the most recent snapshots up to the `limit`, with index 0 being the most recent.
        """
        n_to_return = len(self.snapshots) if limit > len(self.snapshots) else limit
        return sort_snapshots(self.snapshots)[:n_to_return]

    def get_recent_transactions(self, limit: int) -> List[Transaction]:
        """
        Returns a list of the most recent transactions up to the `limit`, with index 0 being the most recent.
        """
        n_to_return = len(self.transactions) if limit > len(self.transactions) else limit
        return sort_transactions(self.transactions)[:n_to_return]

    def get_most_recent_snapshot(self) -> Optional[Snapshot]:
        """
        :return: The most recent snapshot.
        """
        most_recent = self.get_recent_snapshots(1)
        return most_recent[0] if most_recent else None

    def get_most_recent_transaction(self) -> Optional[Transaction]:
        """
        :return: The most recent transaction.
        """
        most_recent = self.get_recent_transactions(1)
        return most_recent[0] if most_recent else None

    def get_net_contribution(self) -> float:
        """
        :return: The net transaction made by an owner.
        """
        return sum([trans.amount for trans in self.transactions])

    def get_contribution_volume(self) -> float:
        """
        :return: The total volume of transactions made by the owner.
        """
        return sum([abs(trans.amount) for trans in self.transactions])

    def get_latest_update_time(self) -> Optional[datetime]:
        """
        :return: The last timestamp recorded for either a transaction or snapshot.
        """
        most_recent_transaction = self.get_most_recent_transaction()
        most_recent_snapshot = self.get_most_recent_snapshot()

        if most_recent_snapshot and most_recent_transaction:
            return max(most_recent_snapshot.timestamp, most_recent_transaction.date_created)

        elif most_recent_transaction:
            return most_recent_transaction.date_created

        elif most_recent_snapshot:
            return most_recent_snapshot.timestamp

        return self.creation_time
