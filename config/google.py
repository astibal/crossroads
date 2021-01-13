
from flask import request, session

REALM = "github"
INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'


def config():
    import os
    try:
        return {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "authorization_base_url": os.environ["GOOGLE_AUTHORIZATION_BASE_URL"],
            "token_url": os.environ["GOOGLE_TOKEN_URL"],
            "redirect_url": os.environ['GOOGLE_REDIRECT_URL']
        }
    except KeyError as e:
        pass
    return {}


def collect_info(oauth_session):

    info = oauth_session.get(INFO_URL)
    if info.status_code < 200 or info.status_code > 299:
        raise ConnectionError("bad response")

    ip = request.remote_addr

    package = {
        "info": info.json(),
        "realm": REALM,
        "ip": ip,
        "referer": session['referer'],
    }

    return package

