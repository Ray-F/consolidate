import os

from flask import Blueprint
from flask_graphql import GraphQLView
from graphene import (
    ObjectType, String, Schema, Int
)

from main.service.mongo_service import MongoService

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/', methods=('GET', 'POST'))
def api():
    mongo_service = MongoService(os.environ.get("MONGO_URI"), 'pyf-attendance-dev')

    me = mongo_service.database.events.find_one({"title": "Three Kings Christmas"})

    return me

class Query(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "Hello, world!"

class RootQuery(Query, ObjectType):
    pass


graphql_view = GraphQLView.as_view(
    'graphql',
    schema=Schema(query=RootQuery),
    graphiql=True
)
