from flask import Flask
from dotenv import load_dotenv

from .route.main_router import graphql_view
from .route.main_router import bp

from .util.json import MongoJSONEncoder

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.json_encoder = MongoJSONEncoder

    app.register_blueprint(bp)
    app.add_url_rule('/api/graph', view_func=graphql_view)

    return app
