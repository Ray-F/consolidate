from datetime import datetime
from dataclasses import dataclass
from main.domain.common.entities import ValueObject


@dataclass(frozen=True)
class Snapshot(ValueObject):
    """
    A snapshot in time of any asset (account or collection of accounts).

    :param timestamp (datetime): The datetime this snapshot is intended to be for.
    :param amount (float): The cumulative value of the asset at this point in time.
    """
    timestamp: datetime
    amount: float
