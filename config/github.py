def config():
    import os
    try:
        return {
            "client_id": os.environ["GITHUB_CLIENT_ID"],
            "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
            "authorization_base_url": os.environ["GITHUB_AUTHORIZATION_BASE_URL"],
            "token_url": os.environ["GITHUB_TOKEN_URL"],
        }
    except KeyError as e:
        pass
    return {}
