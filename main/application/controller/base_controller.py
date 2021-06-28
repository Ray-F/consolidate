from flask_graphql import GraphQLView

from main.application.controller.graph_controller import schema
from main.util.logging import log_init


class BaseController:

    def __init__(self):
        log_init("base controller")

        self.graph = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
        "A graph representation of the API."
