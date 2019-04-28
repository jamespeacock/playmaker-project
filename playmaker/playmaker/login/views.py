from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
import spotipy
import spotipy.oauth2
import logging
import six.moves.urllib.parse as urllibparse

# Create your views here.
from playmaker.login import services
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

        return redirect('%s?%s' % (url, urlparams))


class SpotifyCallbackView(LoginView):

    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        username = request.GET.get('state').split('username-')[1]

        return services.authenticate(username, auth_code)