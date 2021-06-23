from functools import wraps
from os import environ as env

import flask
from authlib.integrations.flask_client import OAuth
from flask import session
from werkzeug.utils import redirect

from main.util.logging import log_init

# TODO: Add authorisation scopes to `requires_auth` and `authorise` (if needed)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/api/login')

        # FIXME: Determine what perms user has and what level of auth `f` requires, by adding scope param
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

    def authorise(self):
        """
        After a user is authenticated with a user account, we can perform authorisation here. This may involve checking
        our database / other entries to confirm what permissions our current user has and redirecting the user to a
        different page if authorisation is not valid.

        :return:
        """
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
        # FIXME: Change this before production
        redirect_uri = 'http://localhost:5000/api/auth_callback'

        return self.auth0.authorize_redirect(redirect_uri=redirect_uri)
