import logging

from django.db import models

from playmaker.controller.visitors import ActionVisitor
from playmaker.shared.models import SPModel
from playmaker.models import User
from playmaker.songs.models import Song


class Device(SPModel):
    is_active = models.BooleanField()
    is_private_session = models.BooleanField()
    is_restricted = models.BooleanField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    volume_percent = models.IntegerField()


class Queue(models.Model):
    songs = models.ManyToManyField(Song)

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
    me = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    queue = models.OneToOneField(Queue, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def listeners(self):
        return Listener.objects.filter(group=self.group).all()


class Group(models.Model):
    controller = models.OneToOneField(Controller, on_delete=models.DO_NOTHING)


class Listener(models.Model):
    me = models.OneToOneField(User, related_name='as_listener', on_delete=models.DO_NOTHING)
    devices = models.ManyToManyField(Device, related_name='listeners_device', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    _v_cached = None

    @property
    def v(self):
        if self._v_cached is None:
            self._v_cached = ActionVisitor.get_visitor(self.me.sp, self.me.username)
        return self._v_cached

    @property
    def token(self):
        return self.me.token

    def _refresh_devices(self):
        if self.devices is None or self.devices.filter(is_active=True).first() is None:
            devices = []

            for d in self.me.sp.devices()['devices']:
                d['sp_id'] = d.pop('id')
                dev = Device(**d)
                dev.save()
                devices.append(dev)

            self.devices.set(devices)

    def refresh(self):
        self._refresh_devices()

        if self.active_device:
            return True

    @property
    def active_device(self):
        ad = self.devices.filter(is_active=True).first()

        if not ad:
            logging.log("Listener: " + self.me.username + " does not have any active devices.")

        return ad


class Permission(models.Model):  # inherit auth_models.Permission if need be
    actor = models.OneToOneField(Controller, on_delete=models.DO_NOTHING)
    listener = models.OneToOneField(Listener, on_delete=models.DO_NOTHING)
    scope = models.CharField(max_length=256)