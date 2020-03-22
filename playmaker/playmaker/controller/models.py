import logging

from django.db import models

from api.settings import DEFAULT_MS_ADDITION, TURN_OFF_IDLE_CONTROLLERS
from playmaker.controller.visitors import ActionVisitor
from playmaker.models import User
from playmaker.songs.models import Song
from playmaker.songs.serializers import SongSerializer


class Controller(models.Model):
    me = models.OneToOneField(User, related_name='controller', on_delete=models.CASCADE)
    mode = models.CharField(choices=[('broadcast','broadcast'), ('curate','curate')], max_length=128)

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

    def currently_playing(self, detail=False):
        logging.log(logging.INFO, "Checking currently playing for " + str(self.controller.me.username))
        sp_client = self.controller.me.sp
        # TODO need to lock around this to prevent multiple updates
        controller_current_song = sp_client.currently_playing()
        controller_song_uri = controller_current_song['item']['uri'] if controller_current_song else None
        if not controller_song_uri:
            logging.log(logging.ERROR, "No currently playing song for controller.")
            if not self.controller.me.active and TURN_OFF_IDLE_CONTROLLERS:
                self.controller.delete()
            return {}
        if not self.current_song or self.current_song != controller_song_uri:
            self.current_song = controller_song_uri
            self.save()
        # TODO End lock here
        if detail:
            if not controller_current_song or not controller_current_song['item']:
                return {}
            # details = sp_client.audio_features(tracks=[controller_current_song['item']['uri']])
            controller_current_song['item']['position_ms'] =  controller_current_song['progress_ms']
            return SongSerializer(controller_current_song['item']).data

        return self.current_song

    def current_offset(self):
        song = self.controller.me.sp.currently_playing()
        if song and song['item']:
            return song['progress_ms'] + DEFAULT_MS_ADDITION
        return 0

    def contents(self):
        return self.songs.order_by('in_q__position').all()

    def clear(self):
        self.songs.clear()


class SongInQueue(models.Model):
    queue = models.ForeignKey(Queue, null=False, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='in_q', null=False, on_delete=models.CASCADE)
    position = models.IntegerField(null=False, blank=False)


class Group(models.Model):
    controller = models.OneToOneField(Controller, related_name='group', on_delete=models.CASCADE)
    # TODO save tracks played

    @property
    def queue(self):
        return self.controller.queue

    def current_song(self, detail=False):
        return self.queue.currently_playing(detail)

    def current_offset(self):
        return self.queue.current_offset()

    def suggest_next_songs(self):
        return

    def play_suggested_song(self):
        return "spotify:track:7fPuWrlpwDcHm5aHCH5D9t"# uri of next song to play


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


class Permission(models.Model):  # inherit auth_models.Permission if need be
    actor = models.OneToOneField(Controller, on_delete=models.CASCADE)
    listener = models.OneToOneField(Listener, on_delete=models.CASCADE)
    scope = models.CharField(max_length=256)