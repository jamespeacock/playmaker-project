from django.db import models

# Create your models here.
from playmaker.controller.models import Controller
from playmaker.songs.models import Song


class Queue(models.Model):
    songs = models.ManyToManyField(Song, through='SongInQueue')
    current_song = models.CharField(max_length=256, null=True)
    next_pos = models.IntegerField(default=0, blank=False, null=False)
    controller = models.OneToOneField(Controller, related_name='queue', on_delete=models.CASCADE, blank=True, null=True)

    def now_playing(self):
        if self.controller:
            return self.controller.now_playing()
        else:
            return self.current_song # or fetch details(self.current_song)

    def current_offset(self):
        if self.controller:
            return self.controller.current_offset()

    def contents(self):
        return self.songs.order_by('in_q__position').all()

    def clear(self):
        self.songs.clear()


class SongInQueue(models.Model):
    queue = models.ForeignKey(Queue, null=False, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='in_q', null=False, on_delete=models.CASCADE)
    position = models.IntegerField(null=False, blank=False)


class Room(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    controller = models.OneToOneField(Controller, related_name='room', on_delete=models.CASCADE, null=True)
    queue = models.OneToOneField(Queue, related_name='room', on_delete=models.CASCADE)
    # TODO save tracks played
    # TODO move queue here instead of controller.

    # @property
    # def queue(self):
    #     return self.controller.queue

    def current_song(self, detail=True):
        if detail:
            return self.queue.now_playing()
        else:
            return self.queue.current_song if self.queue else self.suggest_next_song()

    def current_offset(self):
        return self.queue.current_offset()

    def suggest_next_song(self):
        return None

    def add_suggested_songs_to_queue(self):
        # add_to_queue("root_user_uuid", "suggested_uris")
        songs = []# generate suggestions
        next_pos = self.queue.next_pos
        for s in songs:
            SongInQueue.objects.create(song=s, queue=self.queue, position=self.queue.next_pos)
            next_pos += 1
        self.queue.next_pos = next_pos
        self.queue.save()
        return len(songs)

    def play_suggested_song(self):
        return "spotify:track:7fPuWrlpwDcHm5aHCH5D9t"# uri of next song to play
