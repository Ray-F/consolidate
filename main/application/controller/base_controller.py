import os

from flask import jsonify
from flask_graphql import GraphQLView
from graphene import Schema

from main.application.controller.dto_mapper import AccountDtoMapper
from main.application.controller.graph_controller import RootQuery
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository


class BaseController:

    def __init__(self):
        self.__account_mapper = AccountDtoMapper()
        self.__account_repo = AccountRepository(MongoService(os.environ.get("MONGO_URI"), 'consolidate-dev'))

        self.graph = GraphQLView.as_view('graphql',
                                         schema=Schema(query=RootQuery),
                                         graphiql=True)
        "A graph representation of the API."

    def display_accounts(self):
        accounts = self.__account_repo.list()
        return jsonify([self.__account_mapper.from_domain_model(account) for account in accounts])