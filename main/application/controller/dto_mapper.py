from main.domain.model.transaction import Transaction
from main.domain.common.domain_mapper import DomainModelMapper
from main.domain.common.entities import Dto
from main.util.localdatetime import parse_isostring_with_tz


class TransactionDto(Dto):

    def __init__(self, transaction_id: str, account_id: str, date_created: str, amount: float):
        super().__init__()

        self.id: str = transaction_id
        self.account_id: str = account_id
        self.date_created: str = date_created
        self.amount: float = amount


class TransactionDtoMapper(DomainModelMapper):

    def from_domain_model(self, transaction: Transaction) -> TransactionDto:
        return TransactionDto(transaction_id=str(transaction.id),
                              account_id=str(transaction.account_id),
                              date_created=transaction.date_created.isoformat(),
                              amount=transaction.amount)

    def to_domain_model(self, model: TransactionDto) -> Transaction:
        return Transaction(transaction_id=model.id,
                           account_id=model.account_id,
                           date_created=parse_isostring_with_tz(model.date_created),
                           amount=model.amount)
