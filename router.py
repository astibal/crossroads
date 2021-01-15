import os
import requests
import json
import base64

from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for, make_response
from flask.json import jsonify

from config import github
from config import google

from config import secrets
from config import callbacks


class CrossRoads:
    def __init__(self):
        self.cfg_github = github.config()
        self.cfg_google = google.config()
        self.cfg_callbacks = callbacks.config()


routing = CrossRoads()
app = Flask(__name__)
app.secret_key = secrets.config()["sessions_key"]
if secrets.config()["insecure"]:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.route("/github/login")
def github_login():
    session['referer'] = request.referrer

    # change args only if valid (session['args'] can be already set by different means)
    if request.args:
        session['args'] = request.args

    if not routing.cfg_github:
        return "Service not available"

    scope = None
    # not needed in github case
    # scope = ['user:email', ]

    github = OAuth2Session(
                client_id=routing.cfg_github["client_id"],
                scope=scope)

    authorization_url, state = github.authorization_url(
                routing.cfg_github["authorization_base_url"])

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


def trigger(package):
    for c in routing.cfg_callbacks:
        if c:
            data = json.dumps(package)

            callback_session = requests.Session()
            callback_response = callback_session.post(url=c, json=data)

            return callback_response.json()


def create_response(package):

    action = trigger(package)
    if action['redirect_method'] == 'raw':
        txt = base64.b64decode(action['raw']).decode('utf8')
        return make_response(txt)

    else:
        return redirect('/error')


@app.route("/github/callback")
def github_callback():

    if not session['oauth_state']:
        return redirect(url_for(github_login))

    github_session = OAuth2Session(
                client_id=routing.cfg_github["client_id"],
                state=session['oauth_state'])

    try:
        token = github_session.fetch_token(token_url=routing.cfg_github["token_url"],
                                           client_secret=routing.cfg_github["client_secret"],
                                           authorization_response=request.url)

    except Exception as e:
        return redirect('/github/login')

    try:
        package = github.collect_info(github_session)
        return create_response(package)

    except Exception as e:
        print(e)
        return redirect('/error')

@app.route('/google/login')
def google_login():
    session['referer'] = request.referrer

    # change args only if valid (session['args'] can be already set by different means)
    if request.args:
        session['args'] = request.args

    if not routing.cfg_google:
        return "Service not available"

    scope = ["https://www.googleapis.com/auth/userinfo.email",
             "https://www.googleapis.com/auth/userinfo.profile"]

    google_session = OAuth2Session(routing.cfg_google['client_id'],
                                   scope=scope,
                                   redirect_uri=routing.cfg_google['redirect_url'])

    authorization_url, state = google_session.authorization_url(
                                routing.cfg_google['authorization_base_url'],
                                access_type='offline',
                                prompt='select_account')

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/google/callback')
def google_callback():
    google_session = OAuth2Session(
        client_id=routing.cfg_google["client_id"],
        state=session['oauth_state'],
        redirect_uri=routing.cfg_google['redirect_url'])

    google_session.fetch_token(
        token_url=routing.cfg_google['token_url'],
        client_secret=routing.cfg_google['client_secret'],
        authorization_response=request.url)

    package = google.collect_info(google_session)
    return create_response(package)


@app.route("/ok", methods=['GET'])
def ok():
    return "OK!"


@app.route("/error", methods=['GET'])
def error():
    return "Yikes, something bad happened."


# This is testing local callback - check config.callbacks: we are pointing to here.
#  Code here can be used as a sample for callback receiver
@app.route("/input", methods=['POST'])
def callback_input():

    # package = json.loads(request.json)
    # print("json.loads")
    # print(package)
    #
    # print("ip: " + package["ip"])
    # print("realm: " + package["realm"])
    # if package["realm"] == "github":
    #     print("email: " + package["info"]["email"])

    return redirect("/ok")


@app.route("/", methods=['GET'])
def index():

    session['args'] = request.args

    return """
    <ul>
        <li><a href="/github/login">GitHub</a></li>
        <li><a href="/google/login">Google</a></li>
    </ul>
    """


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
