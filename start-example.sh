#!/bin/sh

# To make this work, you need to setup oauth application on github.
# Copy client_id and client_secret to variables below.
# Also, github application requires to set up callback to reach back
# this crossroads server.
# http://<server-fqdn>:<port>/github/callback

CALLBACKS="http://cr0ssr0ads.io:5000/input;" \
GITHUB_CLIENT_ID="834534344353453454f8" \
GITHUB_CLIENT_SECRET="e50cbed7b63453453453453453453453453455ca" \
GITHUB_AUTHORIZATION_BASE_URL="https://github.com/login/oauth/authorize" \
GITHUB_TOKEN_URL="https://github.com/login/oauth/access_token" \
 \
GOOGLE_CLIENT_ID="407g45g45g74-nfc8ov45g45g4545lquq2970v.apps.googleusercontent.com" \
GOOGLE_CLIENT_SECRET="Xb6gg454Gjz55FRXlhv4aw" \
GOOGLE_AUTHORIZATION_BASE_URL="https://accounts.google.com/o/oauth2/v2/auth" \
GOOGLE_TOKEN_URL="https://www.googleapis.com/oauth2/v4/token" \
GOOGLE_REDIRECT_URL="http://cr0ssr0ads.io:5000/google/callback" \
python3 router.py
