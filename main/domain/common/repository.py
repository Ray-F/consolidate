from typing import List

from main.domain.common.entities import DomainModel


class Repository:
    """
    Supports access to data from persistent sources.
    """

    def list(self) -> List[DomainModel]:
        """
        Gets all of a particular `DomainModel` and returns them.

        :return: A list of domain models.
        """

    def save(self, entity: DomainModel) -> DomainModel:
        """
        Saves a `DomainModel` to persistent storage.

        :param entity: The domain model to save
        :return: The saved domain model
        """
