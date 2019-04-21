from django.db import models

from playmaker.songs.models import Song


class Playlist(models.Model):
    name = models.CharField(max_length=255, null=False)
    uri = models.CharField(max_length=255, null=False)

    songs = models.ManyToManyField(Song, related_name='playlists')
