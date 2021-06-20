from datetime import datetime

from main.domain.util.entities import DomainModel


class Transaction(DomainModel):

    def __init__(self, transaction_id: str, account_id: str, date_created: datetime, amount: float) -> None:
        """
        A real transaction made by the user into (or out of) an asset account.

        :param transaction_id: Automatically generated ID for any transaction.
        :param account_id: The account that this transaction belongs to.
        :param date_created: The date the transaction was made.
        :param amount: The amount of the transaction (positive or negative to 2 DP).
        """

        super().__init__()

        self.id = transaction_id
        self.account_id = account_id
        self.date_created = date_created
        self.amount = amount
