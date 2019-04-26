# -*- coding: utf-8 -*-

import json

from flask import request, url_for
from rauth import OAuth2Service

from app.extensions import config

google_oauth = OAuth2Service(
    name='google',
    client_id=config.get('GOOGLE_CLIENT_ID', ''),
    client_secret=config.get('GOOGLE_CLIENT_SECRET', ''),
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    base_url='https://www.googleapis.com/oauth2/v3/userinfo',
    access_token_url='https://www.googleapis.com/oauth2/v4/token'
)


def get_authorize_url():
    return google_oauth.get_authorize_url(
        scope='email',
        response_type='code',
        redirect_uri=url_for('user.google_callback', _external=True, _scheme=request.scheme)
    )


def new_google_decoder(payload):
    payload = payload.decode('utf-8', "strict")
    payload2 = payload.replace("\n ", '').replace('\n', '')
    return json.loads(payload2)


def verify(code, redirect_url):
    oauth_session = google_oauth.get_auth_session(
        data={'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_url},
        decoder=new_google_decoder
    )

    # , decoder=lambda b: json.loads(str(b))

    me = oauth_session.get('').json()

    if me['email'] is None:
        return False

    return me['email']
