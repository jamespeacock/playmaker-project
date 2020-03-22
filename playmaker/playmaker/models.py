import logging
import time

import spotipy
import uuid as uuid
from django.db.models import DateTimeField
from django.utils import timezone as tz

from django.contrib.auth import models as auth_models
from django.db import models

from api.settings import DEFAULT_INACTIVE_LEN
from playmaker.controller.contants import ID, DEVICE, USER
from playmaker.songs import utils
from playmaker.login import services as logins
from playmaker.songs.models import Artist, Song
from playmaker.shared.models import SPModel


class User(auth_models.AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True, unique=False)
    # TODO figure out how to store this more securely - encryptedField
    access_token = models.CharField(max_length=511, null=True, blank=True)
    refresh_token = models.CharField(max_length=511, null=True, blank=True)
    token_expires = DateTimeField(null=True)
    scope = models.CharField(max_length=511, null=True, blank=True)
    sp_id = models.CharField(max_length=256, null=True, blank=True)
    sp_username = models.CharField(max_length=256, null=True, blank=True)
    is_listener = models.BooleanField(default=False)
    is_controller = models.BooleanField(default=False)
    hasActivePoller = models.BooleanField(default=False)
    pollingThread = models.CharField(null=True, max_length=128)
    last_action = models.FloatField(null=True)
    _sp_cached = None

    @property
    def active(self):
        return (time.time() - self.last_action < DEFAULT_INACTIVE_LEN)

    # make @memoized maybe
    @property
    def actor(self):
        if hasattr(self, 'controller') and self.controller:
            if hasattr(self, 'listener') and self.listener:
                logging.log(logging.WARN, "User has both controller and listener. Deleting listener.")
                self.listener.delete()
                self.save()
            self.is_controller = True
            self.is_listener = False
            self.save()
            return self.controller
        elif hasattr(self, 'listener') and self.listener:
            self.is_listener = True
            self.is_controller = False
            self.save()
            return self.listener
        # logging.log(logging.ERROR, "User %s does not have a listener or a controller!" % self.username) # This is printed out when user first logs in but hasn't selected a role yet, can be a red herring error
        return None

    @property
    def sp(self):
        if self.token and self._sp_cached is None:
            self._sp_cached = spotipy.Spotify(self.token)
        return self._sp_cached

    @property
    def token(self):
        if self.token_expires is None or (self.token_expires - tz.now()).days < 0:
            self._sp_cached = None
            logging.log(logging.INFO, "Refreshing token for: " + str(self.username))
            return logins.do_refresh_token(self)

        return self.access_token or ""

    def save_token(self, token_info):
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.scope = token_info['scope']
        self.token_expires = tz.now() + tz.timedelta(seconds=token_info['expires_in'] - 5)
        self.save()
        return self.info

    def current_song(self):
        cp = self.sp.currently_playing()
        return cp['item']['uri'] if cp and cp['is_playing'] else None

    def play_song(self, uri):
        self.sp.start_playback(device_id=self.active_device.sp_id, uris=[uri])

    @property
    def active_device(self):
        if self.token is None:
            logging.log(logging.INFO, "Lost token for " + self.username)
            return None

        ad = self.devices.filter(is_active=True).first()
        if ad:
            # Should there be a check if this is still the active device?
            return ad

        sd = self.devices.filter(is_selected=True).first()
        if sd:
            return sd

        current_playback = self.sp.current_playback()
        if current_playback:
            current_device = current_playback[DEVICE]
            current_device[USER] = self
            return Device.from_sp(save=True, **current_device)

        logging.log(logging.INFO, "Listener: " + self.username + " does not have any active or selected devices.")
        return None

    def get_devices(self):
        all_ds = []
        for d in self.sp.devices()[Device.get_key()]:
            d[USER] = self
            all_ds.append(Device.from_sp(save=False, **d))
        return all_ds

    def set_device(self, device_id):
        device = self.devices.get(sp_id=device_id)
        if device:
            # Set all other devices for this user to is_selected=False
            for d in self.devices.filter(is_selected=True).all():
                d.is_selected = False
                d.save()
            device.listener = self
            device.is_selected = True
            device.save()
            return True
        else:
            # Fetch current playback and set is_selected device
            logging.log(logging.ERROR, "Selected device for %s was not in database. Fetching now." % self.username)
            for d in self.sp.devices()[Device.get_key()]:
                if d['id'] == device_id:  # d['is_selected'] or d['is_active'] # should these ever take precedent to auto select a device?
                    d[USER] = self
                    Device.from_sp(save=True, **d)
                    return True

        logging.log(logging.ERROR, "Selected device %s was not found for requesting user." % device_id)
        return False

    @property
    def info(self):
        me = self.sp.me()
        null_username = self.sp_username is None
        self.sp_id = me.get(ID)
        # TODO make sp_username unique and throw error here. Give user option to replace user? Maybe don't make it unique but then that can cause other probs
        self.sp_username = me.get('display_name')
        if null_username:
            self.save()
        return me

    @property
    def top_artists(self):
        return utils.from_response(self.sp.current_user_top_artists(), Artist)

    @property
    def top_tracks(self):
        return utils.from_response(self.sp.current_user_top_tracks(), Song)

    @property
    def recently_played(self):
        return utils.from_response(self.sp.current_user_recently_played(), Song)

    @property
    def saved_tracks(self, limit=20, offset=0):
        return utils.from_response(self.sp.current_user_saved_tracks(limit, offset), Song)


class Device(SPModel):
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    is_selected = models.BooleanField(null=True)
    is_active = models.BooleanField(null=True)
    is_private_session = models.BooleanField(null=True)
    is_restricted = models.BooleanField(null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    volume_percent = models.IntegerField(null=True)

    @staticmethod
    def from_sp(save=False, **kwargs):
        kwargs = SPModel.from_sp(kwargs)
        kwargs['is_selected'] = False
        d, _ = Device.objects.get_or_create(
            user=kwargs.pop('user'),
            sp_id=kwargs.pop('sp_id'),
            name=kwargs.pop('name'),
            type=kwargs.pop('type'))
        for k, v in kwargs.items():
            d.__setattr__(k, v)

        if save:
            d.save()
        return d

    @staticmethod
    def get_key():
        return "devices"
