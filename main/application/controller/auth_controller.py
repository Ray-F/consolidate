from functools import wraps
from os import environ as env

import flask
from authlib.integrations.flask_client import OAuth
from flask import session
from werkzeug.utils import redirect

from main.util.logging import log_init


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


class AuthController:

    def __init__(self):
        log_init("base controller")
        oauth = OAuth(flask.current_app)

        base_url = env.get("AUTH0_DOMAIN")
        client_id = env.get("AUTH0_CLIENT_ID")
        client_secret = env.get("AUTH0_CLIENT_SECRET")

        self.auth0 = oauth.register(name='auth0',
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    api_base_url=base_url,
                                    access_token_url=f'{base_url}/oauth/token',
                                    authorize_url=f'{base_url}/authorize',
                                    client_kwargs={'scope': 'openid profile email', })

    def callback_handler(self):
        self.auth0.authorize_access_token()
        resp = self.auth0.get('userinfo')
        userinfo = resp.json()

        session['jwt_payload'] = userinfo

        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }

        return redirect('/')

    def login(self):
        return self.auth0.authorize_redirect(redirect_uri='http://localhost:5000/api/auth_callback')
