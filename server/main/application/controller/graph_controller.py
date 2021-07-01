from os import environ as env

from graphene import ObjectType, String, NonNull, Schema, List, Enum, DateTime, Float, ID, Field, DateTime, Float

from main.application.controller.auth_controller import requires_auth
from main.domain.model.account_aggregate import Account, AccountType
from main.domain.model.user import User
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository
from main.infrastructure.repository.user_repository import UserRepository

mongo_service = MongoService(uri=env.get("MONGO_URI"), db_name='consolidate-dev')
account_repo = AccountRepository(mongo_service=mongo_service)
user_repo = UserRepository(mongo_service=mongo_service, account_repo=account_repo)


class TransactionNode(ObjectType):
    """A transaction."""

    date_created = NonNull(DateTime)
    amount = NonNull(Float)


class SnapshotNode(ObjectType):
    """A snapshot."""

    timestamp = NonNull(DateTime)
    amount = NonNull(Float)


class AccountNode(ObjectType):
    """An account."""

    id = NonNull(ID)
    name = NonNull(String)
    account_type = NonNull(String)
    logo_url = NonNull(String)
    transactions = List(TransactionNode)
    snapshots = List(SnapshotNode)
    net_contribution = NonNull(Float)
    expected_balance = NonNull(Float)
    latest_timestamp = DateTime()
    users = List(lambda: UserNode)
    creation_time = DateTime()

    @staticmethod
    def resolve_logo_url(parent: Account, info):
        return parent.account_type.logo_url

    @staticmethod
    def resolve_net_contribution(parent: Account, info):
        return parent.get_net_contribution()

    @staticmethod
    def resolve_expected_balance(parent: Account, info):
        return parent.get_expected_balance()

    @staticmethod
    def resolve_latest_timestamp(parent: Account, info):
        return parent.get_latest_update_time()

    @staticmethod
    def resolve_users(parent, info):
        users = user_repo.list()

        users_with = filter(lambda user: any([account.id == parent.id for account in user.accounts]), users)
        return users_with


class UserNode(ObjectType):
    """A user."""

    id = NonNull(ID)
    name = NonNull(String)
    email = NonNull(String)
    profile_picture_url = String()
    accounts = List(AccountNode)
    goals = List(SnapshotNode)
    expected_balance = NonNull(Float)
    last_update_time = NonNull(DateTime)

    @staticmethod
    def resolve_profile_picture_url(parent: User, info):
        return parent.profile_picture

    @staticmethod
    def resolve_expected_balance(parent: User, info):
        return parent.get_expected_balance()

    @staticmethod
    def resolve_last_update_time(parent: User, info):
        return parent.get_last_update_time()


class RootQuery(ObjectType):
    """The root of our query."""

    accounts = List(AccountNode, description="Requires authorisation")
    get_account_by_id = Field(AccountNode, id=String(), description="Requires authorisation")

    users = List(UserNode, description="Requires authorisation")
    get_user_by_id = Field(UserNode, id=String(), description="Requires authorisation")

    @staticmethod
    @requires_auth
    def resolve_get_account_by_id(parent, info, id):
        account = account_repo.get_account_by_id(id)
        return account

    @staticmethod
    @requires_auth
    def resolve_accounts(parent, info):
        accounts = account_repo.list()

        return accounts

    @staticmethod
    @requires_auth
    def resolve_users(parent, info):
        users = user_repo.list()
        return users

    @staticmethod
    @requires_auth
    def resolve_get_user_by_id(parent, info, id):
        user = user_repo.get_user_by_id(id)
        return user


schema = Schema(query=RootQuery)
