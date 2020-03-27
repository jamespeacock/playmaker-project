import logging

from django.db import models
from django.db.models import CASCADE

from playmaker.controller.contants import ID, SP_ID, URI, NAME
from playmaker.shared.models import SPModel
from django.core import serializers

from playmaker.songs.services import nice_images


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
    images = models.ManyToManyField(Image, related_name="artist", blank=True)

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
    images = models.ManyToManyField(Image, related_name="album", blank=True)

    def view(self):
        return serializers.serialize('json', self, fields=('name', 'uri', 'images'))

    @staticmethod
    def get_key():
        return "albums"


class Song(SPModel):
    # song title
    name = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artists = models.ManyToManyField(Artist, related_name="songs_rel", blank=True)
    albums = models.ForeignKey(Album, related_name="songs_rel", null=True, blank=True, on_delete=CASCADE)
    uri = models.CharField(max_length=255, null=False)
    duration_ms = models.IntegerField(null=True)
    popularity = models.IntegerField(null=True)
    preview_url = models.CharField(max_length=255, null=True)
    explicit = models.BooleanField(blank=True, default=False)
    track_number = models.IntegerField(null=True, blank=True)
    position_ms = models.IntegerField(null=True)

    # Audio Features
    # key = models.IntegerField(null=True)
    # energy = models.FloatField(null=True)
    # tempo = models.FloatField(null=True)
    # valence = models.FloatField(null=True)
    # danceability = models.FloatField(null=True)
    # mode = models.IntegerField(null=True)
    # acousticness = models.FloatField(null=True)

    # Analysis features TODO
    @property
    def album(self):
        return self.albums.name

    @property
    def position(self):
        in_q = self.__getattribute__('in_q', None)
        if in_q:
            return in_q.position
        return 0

    @property
    def images(self):
        return nice_images(self.album.images['album']['images'])

    @staticmethod
    def pop_kwargs(kwargs):
        for key in ['available_markets', 'disc_number', 'external_ids', 'external_urls', 'type', 'is_local']:
            kwargs.pop(key)

    @staticmethod
    def get_key():
        return "tracks"

    @staticmethod
    def from_sp(details=None, save=False, **kwargs):
        kwargs = SPModel.from_sp(kwargs)
        Song.pop_kwargs(kwargs)
        return Song.create_song(details, save, **kwargs)

    @staticmethod
    def create_song(details, save=False, **song):
        artists = song.pop('artists')
        album = song.pop('album')

        song_obj = Song.objects.filter(sp_id=song[SP_ID]).first()
        if song_obj:
            return song_obj
        else:
            song_obj = Song.objects.create(**song)

        if save:
            song_obj.save()
        for artist in artists:
            artist[SP_ID] = artist.pop(ID)
            a, a_created = Artist.objects.get_or_create(name=artist[NAME], uri=artist[URI], sp_id=artist[SP_ID])
            song_obj.artists.add(a)

        album['sp_id'] = album.pop('id')
        alb, _ = Album.objects.get_or_create(name=album[NAME], uri=album[URI], sp_id=album[SP_ID])
        if save:
            alb.save()
        for img in album['images']:
            img_obj, _ = Image.objects.get_or_create(**img)
            alb.images.add(img_obj.id)
        if save:
            alb.save()
        song_obj.on_album = alb

        if details:
            pass

        if save:
            song_obj.save()
        return song_obj
