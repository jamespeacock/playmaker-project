import spotipy
from django.db.models import DateTimeField
from django.http import JsonResponse

from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from django.utils import timezone as tz
from django.utils import timesince

from django.contrib.auth.models import AbstractUser
from django.db import models

from playmaker.controller.models import Device


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    #TODO figure out how to store this more secuely - encryptedField
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_expires = DateTimeField(null=True)
    scope = models.CharField(max_length=255, null=True, blank=True)

    @property
    def token(self):
        if timesince.timesince(tz.now(), self.token_expires) == '0 minutes': # > self.token_expires:
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
        sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                                               SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE,
                                               state='username-' + self.username)

        token_info = sp_oauth.refresh_access_token(self.refresh_token)

        self.save_token(token_info)


class Controller(models.Model):
    me = models.OneToOneField(User, related_name='as_controller', on_delete=models.DO_NOTHING)

    @property
    def listeners(self):
        return self.group.listeners


class Listener(models.Model):
    me = models.OneToOneField(User, related_name='as_listener', on_delete=models.DO_NOTHING)
    devices = models.ManyToManyField(Device, related_name='devices', blank=True)

    @property
    def token(self):
        return self.me.access_token


class Group(models.Model):
    controller = models.OneToOneField(User, related_name='group', on_delete=models.DO_NOTHING)

    listeners = models.ForeignKey(Listener, on_delete=models.CASCADE)