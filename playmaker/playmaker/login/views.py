from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
import spotipy
import spotipy.util as util
import logging
import json
import requests

# Create your views here.
class SpotifyLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', 'None')
        logging.log(logging.INFO, "In spotify login GET %s" % username)

        # Create a Spotify client that can access my saved song information.
        # token = util.prompt_for_user_token(username,
        #                                            SPOTIFY_SCOPE,
        #                                            client_id=SPOTIFY_CLIENT_ID,
        #                                            client_secret=SPOTIFY_CLIENT_SECRET,
        #                                            redirect_uri=SPOTIFY_REDIRECT_URI)
        url = 'https://accounts.spotify.com/authorize?username=%s?scope=%s?client_id=%s?client_secret=%s?redirect_uri=%s' % (username, SPOTIFY_SCOPE, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)

        return redirect(url)
        # print(response)
        # response_data = json.loads(response.text)
        # access_token = response_data["access_token"]
        # refresh_token = response_data["refresh_token"]
        # token_type = response_data["token_type"]
        # expires_in = response_data["expires_in"]
        #
        # logging.log(logging.WARN, expires_in)


        # return HttpResponse(status=200)

