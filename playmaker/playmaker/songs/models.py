from django.db import models


class Song(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

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


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False)


class Playlist(models.Model):
    # name
    name = models.CharField(max_length=255, null=False)

    tracks = models.ManyToManyField(Song,related_name="playlists")


class Artist(models.Model):
    # name
    name = models.CharField(max_length=255, null=False)

    tracks = models.ManyToManyField(Song, related_name="artists")

    genres = models.ManyToManyField(Genre, related_name="artists")
