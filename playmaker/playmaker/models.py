import spotipy
from django.db.models import DateTimeField
from django.http import JsonResponse
from spotipy import SpotifyOAuth

from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from django.utils import timezone as tz
from django.utils import timesince

from django.contrib.auth import models as auth_models
from django.db import models

# TODO FIx these models up, comment out some shit. The migrations are fucked.!

### Users and Groups
from playmaker.songs import utils


class User(auth_models.AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    #TODO figure out how to store this more secuely - encryptedField
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_expires = DateTimeField(null=True)
    scope = models.CharField(max_length=255, null=True, blank=True)
    sp_cached = None

    @property
    def sp(self):
        if self.sp_cached is None:
            self.sp_cached = spotipy.Spotify(self.token)
        return self.sp_cached

    @property
    def token(self):
        if self.token_expires is None or timesince.timesince(tz.now(), self.token_expires) == '0 minutes':
            self.do_refresh_token()
        return self.access_token

    def save_token(self, token_info):
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.scope = token_info['scope']
        self.token_expires = tz.now() + tz.timedelta(seconds=token_info['expires_in'] - 5)
        self.save()

        user_dict = {"access_token": self.access_token,
                     "scope": self.scope,
                     "id": self.id,
                     "username": self.username}

        return JsonResponse(user_dict, safe=False)

    def do_refresh_token(self):
        sp_oauth = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                                               SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE,
                                               state='username-' + self.username)

        token_info = sp_oauth.refresh_access_token(self.refresh_token)

        self.save_token(token_info)

    @property
    def info(self):
        return self.sp.me()

    @property
    def top_artists(self):
        return utils.from_response(self.sp.current_user_top_artists(), utils.ARTIST_LIST)

    @property
    def top_tracks(self):
        return utils.from_response(self.sp.current_user_top_tracks(), utils.SONG_LIST)

    @property
    def recently_played(self):
        return utils.from_response(self.sp.current_user_recently_played(), utils.SONG_LIST)

    @property
    def saved_tracks(self, limit=20, offset=0):
        return utils.from_response(self.sp.current_user_saved_tracks(limit, offset), utils.SONG_LIST)
