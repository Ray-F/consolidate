from datetime import datetime
from enum import Enum
from typing import List

from main.domain.common.entities import DomainModel, ValueObject
from main.domain.common.errors import DomainError
from main.domain.model.snapshot import Snapshot
from main.util.localdatetime import LOCAL_TIMEZONE


class AccountType(Enum):
    """
    The type of account (either platform or asset type, i.e. Money) the account is.
    """

    ASB = "ASB"
    BNZ = "BNZ"
    SHARESIES = "SHARESIES"
    SIMPLICITY = "SIMPLICITY"

    CASH = "CASH"


class Transaction(ValueObject):

    def __init__(self, date_created: datetime, amount: float) -> None:
        """
        A real transaction made by the user into (or out of) an asset account.

        :param date_created: The date the transaction was made.
        :param amount: The amount of the transaction (positive or negative to 2 DP).
        """

        self.date_created: datetime = date_created
        self.amount: float = amount


class Account(DomainModel):

    def __init__(self,
                 id: str,
                 name: str,
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

        :return: the expected balance amount
        """

        # Sort the list of snapshots and take the most recent one
        latest_snapshot = sorted(self.snapshots, key=lambda snapshot: snapshot.timestamp, reverse=True)[0]

        # Get the sum of all transaction amounts between the latest snapshot and now
        def within_snap_and_now(trans: Transaction):
            return latest_snapshot.timestamp < trans.date_created < datetime.now(tz=LOCAL_TIMEZONE)

        transactions_sum = sum([transaction.amount for transaction in filter(within_snap_and_now, self.transactions)])

        return latest_snapshot.amount + transactions_sum

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
