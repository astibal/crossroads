#!/bin/sh

# To make this work, you need to setup oauth application on github.
# Copy client_id and client_secret to variables below.
# Also, github application requires to set up callback to reach back
# this crossroads server.
# http://<server-fqdn>:<port>/github/callback

CALLBACKS="http://localhost:5000/input;" \
GITHUB_CLIENT_ID="834534344353453454f8" \
GITHUB_CLIENT_SECRET="e50cbed7b63453453453453453453453453455ca" \
GITHUB_AUTHORIZATION_BASE_URL="https://github.com/login/oauth/authorize" \
GITHUB_TOKEN_URL="https://github.com/login/oauth/access_token" \
python3 router.py
