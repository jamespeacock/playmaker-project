import spotipy
from django.db import models
from playmaker.shared.models import SPModel
from playmaker.models import User


class Device(SPModel):
    is_active = models.BooleanField()
    is_private_session = models.BooleanField()
    is_restricted = models.BooleanField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    volume_percent = models.IntegerField()


class Controller(models.Model):
    me = models.OneToOneField(User, related_name='as_controller', on_delete=models.DO_NOTHING)

    @property
    def listeners(self):
        return self.group.listeners


class Listener(models.Model):
    me = models.OneToOneField(User, related_name='as_listener', on_delete=models.DO_NOTHING)
    devices = models.ManyToManyField(Device, related_name='listeners_device', blank=True)

    @property
    def token(self):
        return self.me.token

    def refresh_devices(self):
        if self.devices is None or self.devices.filter(is_active=True).first() is None:
            devices = []
            sp = spotipy.Spotify(self.token)
            for d in sp.devices()['devices']:
                d['sp_id'] = d.pop('id')
                dev = Device(**d)
                dev.save()
                devices.append(dev)

            self.devices.set(devices)

    @property
    def current_playing(self):
        return self.me.sp.current_user_playing_track()

    def refresh_listener(self):
        self.refresh_devices()


class Group(models.Model):
    controller = models.OneToOneField(User, related_name='group', on_delete=models.DO_NOTHING)
    listeners = models.ForeignKey(Listener, on_delete=models.CASCADE)

### Permissions

class Permission(models.Model):  # inherit auth_models.Permission if need be
    actor = models.OneToOneField(Controller, on_delete=models.DO_NOTHING)
    listener = models.OneToOneField(Listener, on_delete=models.DO_NOTHING)
    scope = models.CharField(max_length=256)