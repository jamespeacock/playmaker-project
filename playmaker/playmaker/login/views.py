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
import requests

# Create your views here.
class SpotifyLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        # username = kwargs.get('username', 'None')
        username = request.GET.get('username')
        logging.log(logging.INFO, "In spotify login GET %s" % username)

        # Create a Spotify client that can access my saved song information.
        # token = util.prompt_for_user_token(username,
        #                                            SPOTIFY_SCOPE,
        #                                            client_id=SPOTIFY_CLIENT_ID,
        #                                            client_secret=SPOTIFY_CLIENT_SECRET,
        #                                            redirect_uri=SPOTIFY_REDIRECT_URI)
        url = 'https://accounts.spotify.com/authorize?username=%s?scope=%s?client_id=%s?client_secret=%s?redirect_uri=%s' % (username, SPOTIFY_SCOPE, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)

        return redirect(url)

class SpotifyCallbackView():

    def get(self, request, *args, **kwargs):
        print(request.url)
        auth_code = request.url.split("?code=")[1].split("&")[0]

        sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, 'unused_redirect_url',
                                       scope=SPOTIFY_SCOPE)

        token_info = sp_oauth.get_access_token(auth_code)

        #Get user based on username, save token info to User object, return success.
        #Now backend has credentials for logged in user

        return HttpResponse(status=200, data=token_info)