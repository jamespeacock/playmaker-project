import logging

from django.db import models

from playmaker.controller.visitors import ActionVisitor
from playmaker.shared.models import SPModel
from playmaker.models import User
from playmaker.songs.models import Song
from playmaker.songs.utils import to_obj


class Queue(models.Model):
    songs = models.ManyToManyField(Song)

    def contents(self):
        return self.songs

    def next(self):
        ns = self.songs.first()
        self.songs.remove(ns)
        return ns

    def add(self, song):
        self.songs.add(song)
        return True

    def remove(self, song):
        self.songs.remove(song)

    def clear(self):
        self.songs.clear()


class Controller(models.Model):
    me = models.OneToOneField(User, related_name='controller', on_delete=models.CASCADE)
    queue = models.OneToOneField(Queue, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def listeners(self):
        return Listener.objects.filter(group=self.group).all()

    def init(self):
        if not self.queue:
            self.queue = Queue.objects.create()
            self.queue.save()


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
            for d in self.me.sp.devices()['devices']:
                d['sp_id'] = d.pop('id')
                d['listener'] = self
                to_obj(Device, save=True, **d)

    def refresh(self):
        self._refresh_devices()

        if self.active_device:
            return True

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

    # def __str__


class Permission(models.Model):  # inherit auth_models.Permission if need be
    actor = models.OneToOneField(Controller, on_delete=models.CASCADE)
    listener = models.OneToOneField(Listener, on_delete=models.CASCADE)
    scope = models.CharField(max_length=256)