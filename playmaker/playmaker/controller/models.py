import logging

from django.db import models

from playmaker.controller.contants import LISTENER, DEVICE
from playmaker.controller.visitors import ActionVisitor
from playmaker.shared.models import SPModel
from playmaker.models import User
from playmaker.songs.models import Song

# TODO let Controller have two modes - control & follow
# Control means playmaker queue is sent out to listeners and controller is free to listen to different tracks (to prepare)
# Follow means controller does not have to mess with UI and just listens, the app will throw songs out to users upon changes
class Controller(models.Model):
    me = models.OneToOneField(User, related_name='controller', on_delete=models.CASCADE)

    @property
    def listeners(self):
        return Listener.objects.filter(group=self.group).all()


class Queue(models.Model):
    songs = models.ManyToManyField(Song, through='SongInQueue')
    current_song = models.ForeignKey(Song, related_name='in_groups', on_delete=models.DO_NOTHING, null=True)
    next_pos = models.IntegerField(default=0, blank=False, null=False)
    controller = models.OneToOneField(Controller, related_name='queue', on_delete=models.CASCADE, blank=True, null=True)

    def currently_playing(self):
        # TODO need to lock around this to prevent multiple updates
        sp_current_song = self.controller.me.sp.current_user_playing_track()
        if not self.current_song or self.current_song.uri != sp_current_song:
            self.current_song = sp_current_song # from _obj or whatever
            self.save()

        return self.current_song()

    def contents(self):
        return self.songs.order_by('in_q__position').all()

    def clear(self):
        self.songs.clear()


class SongInQueue(models.Model):
    queue = models.ForeignKey(Queue, null=False, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='in_q', null=False, on_delete=models.CASCADE)
    position = models.IntegerField(null=False, blank=False)


class Group(models.Model):
    controller = models.OneToOneField(Controller, on_delete=models.CASCADE)

    @property
    def queue(self):
        return self.controller.queue


class Listener(models.Model):
    me = models.OneToOneField(User, related_name='listener', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='listeners', on_delete=models.CASCADE)
    _v_cached = None

    @property
    def v(self):
        if self._v_cached is None:
            self._v_cached = ActionVisitor.get_visitor(self.me.sp, self.me.username)
        return self._v_cached

    @property
    def token(self):
        return self.me.token

    @property
    def queue(self):
        return self.group.queue

    def _refresh_devices(self):
        if self.devices is None or self.devices.filter(is_selected=True).first() is None:

            current_device = self.me.sp.current_playback()[DEVICE]
            if current_device:
                current_device[LISTENER] = self
                Device.from_sp(save=True, **current_device)

            for d in self.me.sp.devices()[Device.get_key()]:
                d[LISTENER] = self
                Device.from_sp(save=True, **d) # TODO determine if i really want to be saving all the devices even unused.
        return True

    def refresh(self):
        return self._refresh_devices()

    @property
    def active_device(self):
        active = self.devices.filter(is_active=True).all()
        ad = active.first()
        if ad:
            return ad

        selected = self.devices.filter(is_selected=True).all()
        sd = selected.first()
        if sd:
            return sd

        logging.log(logging.INFO, "Listener: " + self.me.username + " does not have any active or selected devices.")
        return None

    def set_device(self, device_uri):
        device = self.devices.get(uri=device_uri)
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
            return False


class Device(SPModel):
    listener = models.ForeignKey(Listener, related_name='devices', on_delete=models.CASCADE)
    is_selected = models.BooleanField()
    is_active = models.BooleanField()
    is_private_session = models.BooleanField()
    is_restricted = models.BooleanField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    volume_percent = models.IntegerField()
    uri = models.CharField(max_length=255, null=True)

    @staticmethod
    def from_sp(save=False, **kwargs):
        kwargs = SPModel.from_sp(kwargs)
        kwargs['is_selected'] = False
        kwargs.pop(LISTENER)
        d,_ = Device.objects.get_or_create(**kwargs)
        if save:
            d.save()
        return d

    @staticmethod
    def get_key():
        return "devices"


class Permission(models.Model):  # inherit auth_models.Permission if need be
    actor = models.OneToOneField(Controller, on_delete=models.CASCADE)
    listener = models.OneToOneField(Listener, on_delete=models.CASCADE)
    scope = models.CharField(max_length=256)