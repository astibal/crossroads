import os
import requests
import json

from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

from config import github
from config import secrets
from config import callbacks


class CrossRoads:
    def __init__(self):
        self.cfg_github = github.config()
        self.cfg_callbacks = callbacks.config()


routing = CrossRoads()
app = Flask(__name__)
app.secret_key = secrets.config()["sessions_key"]
if secrets.config()["insecure"]:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.route("/github/login")
def github_login():
    session['referer'] = request.referrer

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
            requests.post(c, json=data)


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
        trigger(package)

    except Exception as e:
        return redirect('/error')

    # if we came from real site, return there
    if session['referer']:
        return redirect(session['referer'])

    return redirect("/ok")
    # return jsonify(package)




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




if __name__ == "__main__":
    app.debug = True
    app.run()
