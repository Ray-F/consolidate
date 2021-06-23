import os

from flask import jsonify
from flask_graphql import GraphQLView
from graphene import Schema

from main.application.controller.dto_mapper import AccountDtoMapper, SnapshotDtoMapper, UserDtoMapper
from main.application.controller.graph_controller import RootQuery
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository
from main.infrastructure.repository.user_repository import UserRepository


class BaseController:

    def __init__(self):
        self.__account_mapper = AccountDtoMapper()
        self.__snapshot_mapper = SnapshotDtoMapper()
        self.__user_mapper = UserDtoMapper()

        mongo_service = MongoService(os.environ.get("MONGO_URI"), 'consolidate-dev')
        self.__account_repo = AccountRepository(mongo_service=mongo_service)
        self.__user_repo = UserRepository(mongo_service=mongo_service, account_repository=self.__account_repo)

        self.graph = GraphQLView.as_view('graphql',
                                         schema=Schema(query=RootQuery),
                                         graphiql=True)
        "A graph representation of the API."

    def display_accounts(self):
        accounts = self.__account_repo.list()
        return jsonify([self.__account_mapper.from_domain_model(account) for account in accounts])

    def display_users(self):
        users = self.__user_repo.list()
        return jsonify([self.__user_mapper.from_domain_model(user) for user in users])
