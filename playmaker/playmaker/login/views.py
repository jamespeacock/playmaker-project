import json

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
import spotipy
import spotipy.oauth2
import logging
import six.moves.urllib.parse as urllibparse

# Create your views here.
from playmaker.models import User


class SpotifyLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        # username = kwargs.get('username', 'None')
        username = request.GET.get('username')
        logging.log(logging.INFO, "In spotify login GET %s" % username)

        url = 'https://accounts.spotify.com/authorize'
        urlparams = urllibparse.urlencode({'client_id': SPOTIFY_CLIENT_ID,'response_type':'code',
                                           'redirect_uri': SPOTIFY_REDIRECT_URI,'scope': SPOTIFY_SCOPE,
                                           'state': 'username-'+username})

        my_url = redirect('%s?%s' % (url, urlparams))
        return my_url


class SpotifyCallbackView(LoginView):

    def get(self, request, *args, **kwargs):
        #debug this (it did work on notebook)
        auth_code = request.GET.get('code')
        username = request.GET.get('state').split('username-')[1]
        sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                                               SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE, state='username-'+username)
        token_info = sp_oauth.get_access_token(auth_code)

        #Get user based on username, save token info to User object, return success.
        #Now backend has credentials for logged in user

        user, created = User.objects.get_or_create(username=username)
        user.access_token = token_info['access_token']
        user.refresh_token = token_info['refresh_token']
        user.scope = token_info['scope']
        user.save()

        user_dict = {"access_token": user.access_token,
                     "scope": user.scope,
                     "id": user.id,
                     "username": user.username}
        
        return JsonResponse(user_dict, safe=False)

#TODO implement SpotifyRefreshTokenView