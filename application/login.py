import os
import flask
import logging
import functools
import google.oauth2.credentials
import googleapiclient.discovery

from flask import Flask, render_template
from authlib.client import OAuth2Session


ACCESS_TOKEN_URI = os.environ.get("ACCESS_TOKEN_URI", default=False)
AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL", default=False)
AUTHORIZATION_SCOPE = os.environ.get("AUTHORIZATION_SCOPE", default=False)
AUTH_REDIRECT_URI = os.environ.get("AUTH_REDIRECT_URI", default=False)
BASE_URI = os.environ.get("BASE_URI", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)
CLIENT_ID = os.environ.get("CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=False)
AUTH_TOKEN_KEY = os.environ.get("AUTH_TOKEN_KEY", default=False)
AUTH_STATE_KEY = os.environ.get("AUTH_STATE_KEY", default=False)

app = flask.Blueprint('google_auth', __name__)

def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()

def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return functools.update_wrapper(no_cache_impl, view)


@app.route('/login')
@no_cache
def login():
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
  
    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True
    if is_logged_in():
        print("User Signed in\n")
        return render_template('home.html')
    return flask.redirect(uri, code=302)

@app.route('/auth')
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get('state', default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response('Invalid state parameter', 401)
        return response
    
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

    return flask.redirect(HOME_URI, code=302)

@app.route('/logout')
@no_cache
def logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)
    print("User signed out\n")
    return flask.redirect(BASE_URI, code=302)
