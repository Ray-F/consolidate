import os

from flask import jsonify
from flask_graphql import GraphQLView
from graphene import Schema

from main.application.controller.dto_mapper import TransactionDtoMapper
from main.application.controller.graph_controller import RootQuery
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.transaction_repository import TransactionRepository


class BaseController:

    def __init__(self):
        self.__transaction_mapper = TransactionDtoMapper()
        self.__transaction_repo = TransactionRepository(MongoService(os.environ.get("MONGO_URI"), 'consolidate-dev'))

        self.graph = GraphQLView.as_view('graphql',
                                         schema=Schema(query=RootQuery),
                                         graphiql=True)
        "A graph representation of the API."

    def display_accounts(self):
        transactions = self.__transaction_repo.get_all_transactions()

        return jsonify([self.__transaction_mapper.from_domain_model(transaction) for transaction in transactions])

