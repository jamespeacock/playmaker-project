import logging

from playmaker.controller.contants import ARTIST, TRACK
from playmaker.playlists.models import Playlist
from playmaker.songs.models import Artist, Song
from playmaker.songs.serializers import ArtistSerializer, SongSerializer


def get_cls(_t):
    if ARTIST in _t:
        cls, ser = Artist, ArtistSerializer
    elif TRACK in _t:
        cls, ser = Song, SongSerializer
    else:
        raise Warning("Cannot find class: " + str(_t))

    return cls, ser


DONT_SAVE = [Artist, Playlist]


def iterable(s):
    return s + 's'


def to_obj(__type, save=False, **_kwargs):
    if iterable(__type) in _kwargs:
        return [to_obj(__type, save=save, **o) for o in _kwargs.get(iterable(__type))]

    cls, ser = get_cls(__type)
    kwargs = _kwargs.copy()
    kwargs['sp_id'] = kwargs.pop('id')

    if not save or cls in DONT_SAVE:
        return ser(instance=kwargs).data

    if cls == Song:
        # pop from kwargs breaking values
        cls.pop_kwargs(kwargs)
        obj, created = cls.objects.get_or_create(**kwargs)
        logging.log(logging.INFO, "Song: " + obj.name + " was " + "created." if created else "updated.")
        return ser(instance=kwargs).data

    logging.log(logging.INFO, "Wanted to save non song object? NEed to implement.")
    return ser(instance=kwargs).data


def get_key(str_type):
    if str_type == TRACK:
        return "tracks"
    else:
        return str_type


def from_response(spotify_resp, __type):

    response_data = spotify_resp[get_key(__type)]
    return [to_obj(__type, **i) for i in response_data if i] \
        if isinstance(spotify_resp, list)\
        else to_obj(__type, **spotify_resp)


