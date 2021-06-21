from datetime import datetime

from main.domain.common.entities import ValueObject


class Snapshot(ValueObject):

    def __init__(self, date: datetime, amount: float) -> None:
        super().__init__()

        self.date = date
        self.amount = amount
