from datetime import datetime
from typing import List

from main.domain.common.entities import DomainModel
from main.domain.model.account_aggregate import Account
from main.domain.model.snapshot import Snapshot


class User(DomainModel):

    def __init__(self,
                 id: str,
                 name: str,
                 email: str,
                 profile_picture: str,
                 # TODO: Make accounts permission based.
                 accounts: List[Account],
                 goals: [Snapshot]):
        """
        A User that owns or has access to accounts, and can log in to our services.

        :param id: Automatically generated user identifier.
        :param name: Full name of the user (or human readable identification).
        :param email: Email address.
        :param profile_picture: Url to the profile picture.
        :param accounts: List of accounts the user has access to.
        :param goals: Saving or asset goals (as Snapshots at points in time, usually in the future).
        """

        self.id: str = id
        self.name: str = name
        self.email: str = email
        self.profile_picture: str = profile_picture
        self.accounts: List[Account] = accounts
        self.goals: List[Snapshot] = goals

    def get_expected_balance(self) -> float:
        """
        :return: The most accurate value for user's existing asset value.
        """
        return sum([account.get_expected_balance() for account in self.accounts])

    def get_last_update_time(self) -> datetime:
        """
        :return: The last update time of the user.
        """
        # FIXME: Implement this
        accounts = self.accounts
        return datetime.now()
