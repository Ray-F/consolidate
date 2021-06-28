from typing import Any

from main.domain.common.entities import DomainModel, ValueObject


class DomainModelMapper:

    def from_domain_model(self, domain_model: DomainModel) -> Any:
        """
        Converts a domain model to any other model (i.e. Entity, DTO).

        :param domain_model: The model to convert.
        :return: The other model.
        """

    def to_domain_model(self, model: Any) -> DomainModel:
        """
        Converts an entity, DTO or other data model into a Domain Model.

        :param model: the other model to convert into a Domain Model.
        :return: The domain model.
        """


class ValueObjectMapper:

    def from_object(self, value_object: ValueObject) -> Any:
        """
        Converts a value object to any other model.

        :param value_object: The value object to convert.
        :return: The other model
        """

    def to_object(self, model: Any) -> ValueObject:
        """
        Converts an entity, DTO or other data model into a Value Object.

        :param model: The other model to convert into a value object.
        :return: The value object
        """
