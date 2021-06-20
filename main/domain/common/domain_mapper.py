from typing import Any

from main.domain.common.entities import DomainModel


class DomainModelMapper:

    def from_domain_model(self, domain_model: DomainModel) -> Any:
        """
        Converts a domain model to any other model (i.e. Entity, DTO).

        :param domain_model: The model to convert.
        :return: The other model.
        """
        pass

    def to_domain_model(self, model: Any) -> DomainModel:
        """
        Converts an entity, DTO or other data model into a Domain Model.

        :param model: the other model to convert into a Domain Model.
        :return: The domain model.
        """
        pass
