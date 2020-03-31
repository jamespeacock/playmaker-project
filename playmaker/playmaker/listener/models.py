from django.db import models
from playmaker.controller.visitors import ActionVisitor
from playmaker.models import User
from playmaker.rooms.models import Room


class Listener(models.Model):
    me = models.OneToOneField(User, related_name='listener', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='listeners', on_delete=models.CASCADE, null=True)
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
        return self.room.queue if self.room else []

    @property
    def username(self):
        return self.me.username