import logging

from django.db import models

from playmaker.controller.contants import LISTENER
from playmaker.controller.visitors import ActionVisitor
from playmaker.shared.models import SPModel
from playmaker.models import User
from playmaker.songs.models import Song


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
        if self.devices is None or self.devices.filter(is_active=True).first() is None:
            for d in self.me.sp.devices()[Device.get_key()]:
                d[LISTENER] = self
                Device.from_sp(save=True, **d)

    def refresh(self):
        self._refresh_devices()

    @property
    def active_device(self):
        opts = self.devices.filter(is_active=True).all()
        ad = opts.first()
        if len(opts) > 1:

            phones = opts.filter(name__contains='Phone')
            ad = phones.first() if len(phones) > 0 else opts.first()

        if not ad:
            logging.log(logging.INFO, "Listener: " + self.me.username + " does not have any active devices.")

        return ad


class Device(SPModel):
    listener = models.ForeignKey(Listener, related_name='devices', on_delete=models.CASCADE)
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