from datetime import datetime
from dataclasses import dataclass
from typing import List

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


def sort_snapshots(snapshots_list: List[Snapshot]) -> List[Snapshot]:
    """
    Sorts a list of snapshots in order of the most recent (index 0) to oldest (index -1).

    :param snapshots_list: The list of snapshots to sort.
    :return: A sorted list of snapshots.
    """
    return sorted(snapshots_list, key=lambda x: x.timestamp, reverse=True)
