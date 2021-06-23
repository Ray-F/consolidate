from flask import Blueprint

from main.application.controller.auth_controller import AuthController
from main.application.controller.base_controller import BaseController


bp = Blueprint('api', __name__, url_prefix='/api')

# Application related routing

base_control = BaseController()

bp.add_url_rule(rule='/accounts', view_func=base_control.display_accounts)
bp.add_url_rule(rule='/users', view_func=base_control.display_users)

bp.add_url_rule(rule='/graph', view_func=base_control.graph)

# Authentication related routing

auth_control = AuthController()

bp.add_url_rule(rule='/auth_callback', view_func=auth_control.authorise)
bp.add_url_rule(rule='/login', view_func=auth_control.login)
