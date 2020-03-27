import logging

from django.db import models

from api.settings import DEFAULT_MS_ADDITION, TURN_OFF_IDLE_CONTROLLERS
from playmaker.models import User
from playmaker.songs.models import Song
from playmaker.songs.serializers import SongSerializer
from playmaker.songs.services import align_sp_song


class Controller(models.Model):
    me = models.OneToOneField(User, related_name='controller', on_delete=models.CASCADE)
    mode = models.CharField(choices=[('broadcast','broadcast'), ('curate','curate')], max_length=128)

    def __str__(self):
        return 'ID: {} - username: {}'.format(self.id, self.me.username)

    @property
    def listeners(self):
        return self.room.listeners.all()

    @property
    def username(self):
        return self.me.username


class Queue(models.Model):
    songs = models.ManyToManyField(Song, through='SongInQueue')
    current_song = models.CharField(max_length=256, null=True)
    next_pos = models.IntegerField(default=0, blank=False, null=False)
    controller = models.OneToOneField(Controller, related_name='queue', on_delete=models.CASCADE, blank=True, null=True)

    def now_playing(self):
        logging.log(logging.INFO, "Checking currently playing for " + str(self.controller.me.username))
        sp_client = self.controller.me.sp
        # TODO need to lock around this to prevent multiple updates
        controller_current_song = sp_client.currently_playing()
        controller_song_uri = controller_current_song['item']['uri'] if controller_current_song else None
        if not controller_song_uri:
            logging.log(logging.ERROR, "No currently playing song for controller.")
            if not self.controller.me.active and TURN_OFF_IDLE_CONTROLLERS:
                self.controller.delete()
            return None
        if not self.current_song or self.current_song != controller_song_uri:
            self.current_song = controller_song_uri
            self.save()
        # TODO End lock here
            if not controller_current_song or not controller_current_song['item']:
                return None

        response_song = align_sp_song(controller_current_song)
        return SongSerializer(response_song).data

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


# class Group(models.Model):
#     name = models.CharField(max_length=255, null=True, blank=False)
#     controller = models.OneToOneField(Controller, related_name='group', on_delete=models.CASCADE)
#     # TODO save tracks played
#
#     @property
#     def queue(self):
#         return self.controller.queue
#
#     def current_song(self, detail=False):
#         if detail:
#             return self.queue.now_playing()
#         else:
#             return self.queue.current_song if self.queue else None
#
#     def current_offset(self):
#         return self.queue.current_offset()
#
#     def suggest_next_songs(self):
#         return
#
#     def play_suggested_song(self):
#         return "spotify:track:7fPuWrlpwDcHm5aHCH5D9t"# uri of next song to play

