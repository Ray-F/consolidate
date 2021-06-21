from dotenv import load_dotenv
from flask import Flask

from main.application.route.main_router import bp
from main.util.json import DtoJsonEncoder

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = DtoJsonEncoder
    app.register_blueprint(bp)

    return app
