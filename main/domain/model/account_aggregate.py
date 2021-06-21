from datetime import datetime
from enum import Enum

from main.domain.common.entities import DomainModel, ValueObject
from typing import List


class AccountType(Enum):

    ASB = "ASB"
    BNZ = "BNZ"
    SHARESIES = "SHARESIES"
    SIMPLICITY = "SIMPLICITY"


class Snapshot(ValueObject):

    def __init__(self, date: datetime, amount: float) -> None:
        super().__init__()

        self.date = date
        self.amount = amount


class Transaction(ValueObject):

    def __init__(self, date_created: datetime, amount: float) -> None:
        """
        A real transaction made by the user into (or out of) an asset account.

        :param date_created: The date the transaction was made.
        :param amount: The amount of the transaction (positive or negative to 2 DP).
        """

        super().__init__()

        self.date_created = date_created
        self.amount = amount


class Account(DomainModel):

    def __init__(self,
                 account_id: str,
                 name: str,
                 account_type: AccountType,
                 transactions: List[Transaction],
                 snapshots: List[Snapshot]) -> None:
        """
        An asset account.

        :param account_id: A unique ID for all accounts (automatically generated).
        :param name: A human readable name (provided by the user) of the account.
        :param account_type: The account type.
        :param transactions: List of all transactions made for this account.
        :param snapshots: List of all account snapshots.
        """

        super().__init__()

        self.id = account_id
        self.name = name
        self.account_type = account_type
        self.transactions = transactions
        self.snapshots = snapshots

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def add_snapshot(self, snapshot: Snapshot):
        self.snapshots.append(snapshot)

    def get_latest_balance(self) -> float:
        return self.snapshots[-1].amount

    def get_contribution(self) -> float:
        return sum([trans.amount for trans in self.transactions])