from django.db import models

from playmaker.shared.models import SPModel


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
    genres = models.ManyToManyField(Genre, related_name="artists")
    num_followers = models.IntegerField(null=True)
    images = models.ManyToManyField(Image, related_name="artist_images")


class Album(SPModel):
    artists = models.ManyToManyField(Artist)


class Song(SPModel):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.ManyToManyField(Artist)
    uri = models.CharField(max_length=255, null=False)

    # Audio Features
    key = models.FloatField(null=False)
    energy = models.FloatField(null=False)
    tempo = models.FloatField(null=False)
    valence = models.FloatField(null=False)
    danceability = models.FloatField(null=False)
    acousticness = models.FloatField(null=False)

    # Less impt
    loudness = models.FloatField(null=False)
    mode = models.BooleanField(null=False)
    duration_ms = models.FloatField(null=False)

    # Analysis features TODO

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)






