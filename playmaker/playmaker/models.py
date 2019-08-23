import spotipy
import uuid as uuid
from django.db.models import DateTimeField
from django.http import JsonResponse
from django.utils import timezone as tz
from django.utils import timesince

from django.contrib.auth import models as auth_models
from django.db import models

from playmaker.controller.contants import TRACK, ARTIST
from playmaker.songs import utils
from playmaker.login import services as logins


class User(auth_models.AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True, unique=False)
    # TODO figure out how to store this more secuely - encryptedField
    access_token = models.CharField(max_length=511, null=True, blank=True)
    refresh_token = models.CharField(max_length=511, null=True, blank=True)
    token_expires = DateTimeField(null=True)
    scope = models.CharField(max_length=511, null=True, blank=True)
    sp_id = models.CharField(max_length=256, null=True, blank=True)
    sp_username = models.CharField(max_length=256, null=True, blank=True)
    _sp_cached = None

    @property
    def actor(self):
        if self.listener:
            return self.listener
        elif self.controller:
            return self.controller
        else:
            return self

    @property
    def sp(self):
        if self.token and self._sp_cached is None:
            self._sp_cached = spotipy.Spotify(self.token)
        return self._sp_cached

    @property
    def token(self):
        if self.token_expires is None or timesince.timesince(tz.now(), self.token_expires) == '0 minutes':
            self._sp_cached = None
            return logins.do_refresh_token(self)

        return self.access_token

    def save_token(self, token_info):
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.scope = token_info['scope']
        self.token_expires = tz.now() + tz.timedelta(seconds=token_info['expires_in'] - 5)
        self.save()
        return self.info

    @property
    def info(self):
        me = self.sp.me()
        self.sp_id = me.get('id')
        # TODO make sp_username unique and throw error here. Give user option to replace user? Maybe don't make it unique but then that can cause other probs
        self.sp_username = me.get('display_name')
        return me

    @property
    def top_artists(self):
        return utils.from_response(self.sp.current_user_top_artists(), ARTIST)

    @property
    def top_tracks(self):
        return utils.from_response(self.sp.current_user_top_tracks(), TRACK)

    @property
    def recently_played(self):
        return utils.from_response(self.sp.current_user_recently_played(), TRACK)

    @property
    def saved_tracks(self, limit=20, offset=0):
        return utils.from_response(self.sp.current_user_saved_tracks(limit, offset), TRACK)
