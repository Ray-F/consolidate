from dotenv import load_dotenv
from flask import Flask

from main.application.route.main_router import bp
from .util.json import MongoJSONEncoder

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.json_encoder = MongoJSONEncoder
    app.register_blueprint(bp)

    return app
