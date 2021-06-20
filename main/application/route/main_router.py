from flask import Blueprint

from main.application.controller.base_controller import BaseController

bp = Blueprint('api', __name__, url_prefix='/api')

controller = BaseController()

bp.add_url_rule(rule='/list',
                methods=('GET', 'POST'),
                view_func=controller.display_accounts)

bp.add_url_rule(rule='/graph',
                view_func=controller.graph)
