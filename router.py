import os

from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

from config import github
from config import secrets


class CrossRoads:
    def __init__(self):
        self.cfg_github = github.config()


routing = CrossRoads()
app = Flask(__name__)
app.secret_key = secrets.config()["sessions_key"]
if secrets.config()["insecure"]:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.route("/github/login")
def github_login():
    if not routing.cfg_github:
        return "Service not available"

    scope = None
    # not needed in github case
    scope = ['user:email', ]

    github = OAuth2Session(
                client_id=routing.cfg_github["client_id"],
                scope=scope)

    authorization_url, state = github.authorization_url(
                routing.cfg_github["authorization_base_url"])

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/github/callback")
def github_callback():
    github = OAuth2Session(
                client_id=routing.cfg_github["client_id"],
                state=session['oauth_state'])

    token = github.fetch_token(token_url=routing.cfg_github["token_url"], client_secret=routing.cfg_github["client_secret"],
                               authorization_response=request.url)

    return jsonify(github.get('https://api.github.com/user').json())


if __name__ == "__main__":
    app.debug=True
    app.run()