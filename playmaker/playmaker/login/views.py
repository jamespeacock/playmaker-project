from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import logging
import json
import base64
import requests
import six
import six.moves.urllib.parse as urllibparse

# Create your views here.
class SpotifyLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        # username = kwargs.get('username', 'None')
        username = request.GET.get('username')
        logging.log(logging.INFO, "In spotify login GET %s" % username)

        url = 'https://accounts.spotify.com/authorize?'
        urlparams = urllibparse.urlencode({'username': username, 'scope': SPOTIFY_SCOPE, 'client_id': SPOTIFY_CLIENT_ID,
                                           'client_secret': SPOTIFY_CLIENT_SECRET,'redirect_uri': SPOTIFY_REDIRECT_URI,
                                           'response_type':'code'})

        return redirect('%s:%s' % (url, urlparams))

class SpotifyCallbackView(LoginView):

    def get(self, request, *args, **kwargs):
        #debug this (it did work on notebook)
        auth_code = request.GET.get('code')
        sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, 'http://localhost',
                                                 scope=SPOTIFY_SCOPE)
        token_info = sp_oauth.get_access_token(auth_code)

        # token_info = get_access_token(auth_code, SPOTIFY_REDIRECT_URI, SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_SECRET, scope=SPOTIFY_SCOPE)

        #Get user based on username, save token info to User object, return success.
        #Now backend has credentials for logged in user

        return HttpResponse(status=200)


OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

def get_access_token(code, redirect_uri, client_id, client_secret, scope=None, state=None):
    payload = {'redirect_uri': redirect_uri,
               'code': code,
               'grant_type': 'authorization_code'}
    if scope:
        payload['scope'] = scope
    if state:
        payload['state'] = state

    auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii'), 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(OAUTH_TOKEN_URL, data=payload,
                             headers=headers, verify=True)
    if response.status_code != 200:
        raise Exception(response.reason)
    token_info = response.json()
    # token_info = self._add_custom_values_to_token_info(token_info)
    # self._save_token_info(token_info)
    return token_info