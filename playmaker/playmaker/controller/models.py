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

    def now_playing(self):
        user = self.me
        logging.log(logging.INFO, "Checking currently playing for " + str(user.username))
        sp_client = user.sp
        # TODO need to lock around this to prevent multiple updates
        controller_current_song = sp_client.currently_playing()
        controller_song_uri = controller_current_song['item']['uri'] if controller_current_song and controller_current_song['item'] else None
        if not controller_song_uri:
            logging.log(logging.ERROR, "No currently playing song for controller.")
            if not user.active and TURN_OFF_IDLE_CONTROLLERS:
                user.is_controller = False
                user.save()
                logging.log(logging.INFO, "Deleting Idle/Exited Controller for: " + user.username)
                user.controller.delete()

            return None
        if not self.current_song or self.current_song != controller_song_uri:
            self.queue.current_song = controller_song_uri
            logging.log(logging.INFO, "Updating song for: " + user.username + " | is_controller: " + str(user.is_controller))
            print("Updating song for: " + user.username + " | is_controller: " + str(user.is_controller))
            self.queue.save()
        # TODO End lock here
            if not controller_current_song or not controller_current_song['item']:
                return None

        response_song = align_sp_song(controller_current_song)
        return SongSerializer(response_song).data

    def current_offset(self):
        song = self.me.sp.currently_playing()
        if song and song['item']:
            return song['progress_ms'] + DEFAULT_MS_ADDITION
        return 0

    @property
    def current_song(self):
        return self.queue.current_song