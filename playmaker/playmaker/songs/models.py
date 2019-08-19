from django.db import models

from playmaker.shared.models import SPModel
from .services import to_song_view, to_artist_view
from django.core import serializers


class Image(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.CharField(max_length=255)


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False)

    # TODO how to make a genre node network oooohh


class Artist(SPModel):
    # name
    name = models.CharField(max_length=255, null=False)
    popularity = models.IntegerField(null=True)
    uri = models.CharField(max_length=255, null=True)
    genres = models.ManyToManyField(Genre, related_name="artists", blank=True)
    num_followers = models.IntegerField(null=True)
    images = models.ManyToManyField(Image, related_name="artist_images", blank=True)

    def view(self):
        return {"name": self.name}


class Album(SPModel):
    name = models.CharField(max_length=255, null=False)
    artists = models.ManyToManyField(Artist, blank=True)

    def view(self):
        return to_artist_view(serializers.serialize('json', self, fields=('name', 'uri')))


class Song(SPModel):
    # song title
    name = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artists = models.ManyToManyField(Artist, related_name="songs", blank=True)
    album = models.ManyToManyField(Album, related_name="songs", blank=True)
    uri = models.CharField(max_length=255, null=False)
    duration_ms = models.FloatField(null=True)
    popularity = models.FloatField(null=True)
    preview_url = models.CharField(max_length=255, null=True)

    # Audio Features
    # key = models.FloatField(null=False)
    # energy = models.FloatField(null=False)
    # tempo = models.FloatField(null=False)
    # valence = models.FloatField(null=False)
    # danceability = models.FloatField(null=False)
    # acousticness = models.FloatField(null=False)
    #
    # # Less impt
    # loudness = models.FloatField(null=False)
    # mode = models.BooleanField(null=False)
    # duration_ms = models.FloatField(null=False)

    # Analysis features TODO

    def __str__(self):
        return "{} - {}".format(self.name, ','.join([a.name for a in self.artists.all()]))

    def view(self):
        # Can update this as more info from song is incorporated into frontend
        return serializers.serialize('json', self, fields=('name', 'artist', 'uri'))




