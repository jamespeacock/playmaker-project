from django.db import models

# Create your models here.
from playmaker.controller.models import Controller


class Room(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    controller = models.OneToOneField(Controller, related_name='room', on_delete=models.CASCADE)
    # TODO save tracks played

    @property
    def queue(self):
        return self.controller.queue

    def current_song(self, detail=True):
        if detail:
            return self.queue.now_playing()
        else:
            return self.queue.current_song if self.queue else None

    def current_offset(self):
        return self.queue.current_offset()

    def suggest_next_songs(self):
        return

    def play_suggested_song(self):
        return "spotify:track:7fPuWrlpwDcHm5aHCH5D9t"# uri of next song to play
