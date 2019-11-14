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

    def __str__(self):
        return 'ID: {} - username: {}'.format(self.id, self.me.username)

    @property
    def listeners(self):
        return Listener.objects.filter(group=self.group).all()


class Queue(models.Model):
    songs = models.ManyToManyField(Song, through='SongInQueue')
    current_song = models.CharField(max_length=256, null=True)
    next_pos = models.IntegerField(default=0, blank=False, null=False)
    controller = models.OneToOneField(Controller, related_name='queue', on_delete=models.CASCADE, blank=True, null=True)

    def currently_playing(self):
        # TODO need to lock around this to prevent multiple updates
        controller_current_song = self.controller.me.sp.currently_playing()
        controller_song_uri = controller_current_song['item']['uri'] if controller_current_song else None
        if not self.current_song or self.current_song != controller_song_uri:
            self.current_song = controller_song_uri # from _obj or whatever
            self.save()

        return self.current_song

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

    def current_song(self):
        return self.queue.currently_playing()


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

            current_playback = self.me.sp.current_playback()
            if current_playback:
                current_device = current_playback[DEVICE]
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
            return False
        self.refresh()  # TODO test if this is necessary



    def current_song(self):
        return self.sp.currently_playing()['uri']


class Device(SPModel):
    listener = models.ForeignKey(Listener, related_name='devices', on_delete=models.CASCADE)
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
        logging.log(logging.ERROR, str(kwargs))
        d,_ = Device.objects.get_or_create(
            listener_id=kwargs.pop('listener'),
            sp_id=kwargs.pop('sp_id'),
            name=kwargs.pop('name'),
            type=kwargs.pop('type'))
        d.update(**kwargs)
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