from datetime import datetime

from main.domain.common.entities import ValueObject


class Snapshot(ValueObject):

    def __init__(self, timestamp: datetime, amount: float) -> None:
        """
        A snapshot in time of any asset (account or collection of accounts).
        
        :param timestamp: The datetime this snapshot is intended to be for.
        :param amount: The cumulative value of the asset at this point in time.
        """

        self.timestamp: datetime = timestamp
        self.amount: float = amount
