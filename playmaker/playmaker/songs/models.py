import logging

from django.db import models

from playmaker.controller.contants import ID, SP_ID, URI, NAME
from playmaker.shared.models import SPModel
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
        return serializers.serialize('json', self, fields=('name',))

    @staticmethod
    def get_key():
        return "artists"

    @staticmethod
    def from_sp(save=False, **kwargs):
        raise NotImplementedError()


class Album(SPModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)
    uri = models.CharField(max_length=255, null=True)

    def view(self):
        return serializers.serialize('json', self, fields=('name', 'uri'))

    @staticmethod
    def get_key():
        return "albums"


class Song(SPModel):
    # song title
    name = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artists = models.ManyToManyField(Artist, related_name="songs", blank=True)
    album = models.ManyToManyField(Album, related_name="songs", blank=True)
    uri = models.CharField(max_length=255, null=False)
    duration_ms = models.IntegerField(null=True)
    popularity = models.IntegerField(null=True)
    preview_url = models.CharField(max_length=255, null=True)
    explicit = models.BooleanField(blank=True, default=False)
    track_number = models.IntegerField(null=True, blank=True)

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

    def view(self):
        # Can update this as more info from song is incorporated into frontend
        return serializers.serialize('json', [self], fields=('name', 'artist', 'uri'))

    @staticmethod
    def pop_kwargs(kwargs):
        for key in ['available_markets', 'disc_number', 'external_ids', 'external_urls', 'type', 'is_local']:
            kwargs.pop(key)

    @staticmethod
    def get_key():
        return "tracks"


    @staticmethod
    def from_sp(save=False, **kwargs):
        kwargs = SPModel.from_sp(kwargs)
        Song.pop_kwargs(kwargs)
        artists = kwargs.pop('artists')
        album = kwargs.pop('album')
        song = Song.objects.filter(sp_id=kwargs[SP_ID]).first()
        if song:
            # TODO is this necessary - preview url only comes back from search
            song = Song(pk=song.pk, **kwargs)
            song.save()
            created = False
        else:
            song = Song.objects.create(**kwargs)
            created = True
        # album['sp_id'] = album.pop('id')
        # alb, alb_created = Album.objects.get_or_create(name=album['name'], uri=album['uri'], sp_id=album['sp_id'])
        # obj.album = alb

        for artist in artists:
            artist[SP_ID] = artist.pop(ID)
            a, a_created = Artist.objects.get_or_create(name=artist[NAME], uri=artist[URI], sp_id=artist[SP_ID])
            song.artists.add(a)

        song.save()
        logging.log(logging.INFO, "Song: " + song.name + " was " + "created." if created else "updated.")
        return song
