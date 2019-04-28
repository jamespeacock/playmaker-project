import spotipy
from django.db.models import DateTimeField
from django.http import JsonResponse

from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from django.utils import timezone as tz
from django.utils import timesince

from django.contrib.auth import models as auth_models
from django.db import models

from playmaker.controller.models import Device

### Users and Groups

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

    def top_artists(self):
        return self.sp.current_user_top_artists()

    def top_tracks(self):
        return self.sp.current_user_top_tracks()


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

    def get_devices(self):
        if self.devices.blank is True or self.devices.filter(is_active=True).first() is not None:
            devices = []
            sp = spotipy.Spotify(self.token)
            for d in sp.devices()['devices']:
                d['sp_id'] = d.pop('id')
                dev = Device(**d)
                dev.save()
                devices.append(dev)

            self.devices.set(devices)

    def top_artists(self):
        return self.me.top_artists()

    def recent_artists(self):
        return self.me.recent_artists()

    def refresh_user(self):
        return self.me.refresh_user()


class Group(models.Model):
    controller = models.OneToOneField(User, related_name='group', on_delete=models.DO_NOTHING)

    listeners = models.ForeignKey(Listener, on_delete=models.CASCADE)


### Permissions

class Permission(auth_models.Permission):
    actor = models.OneToOneField(Controller, on_delete=models.DO_NOTHING)
    listener = models.OneToOneField(Listener, on_delete=models.DO_NOTHING)
    scope = models.CharField(max_length=256)

