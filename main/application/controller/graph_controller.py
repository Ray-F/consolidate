from os import environ as env

from graphene import ObjectType, String, NonNull, Schema, List, Enum, DateTime, Float, ID, Field

from main.domain.model.account_aggregate import AccountType
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
    account_type = NonNull(Enum.from_enum(AccountType))
    transactions = List(TransactionNode)
    snapshots = List(SnapshotNode)

    users = List(lambda: UserNode)

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

    @staticmethod
    def resolve_profile_picture_url(parent, info):
        return parent.profile_picture


class RootQuery(ObjectType):
    """The root of our query."""

    accounts = List(AccountNode)
    get_account_by_id = Field(AccountNode, id=String())

    users = List(UserNode)
    get_user_by_id = Field(UserNode, id=String())

    @staticmethod
    def resolve_get_account_by_id(parent, info, id):
        account = account_repo.get_account_by_id(id)
        return account

    @staticmethod
    def resolve_accounts(parent, info):
        accounts = account_repo.list()

        return accounts

    @staticmethod
    def resolve_users(parent, info):
        users = user_repo.list()
        return users

    @staticmethod
    def resolve_get_user_by_id(parent, info, id):
        user = user_repo.get_user_by_id(id)
        return user


schema = Schema(query=RootQuery)
