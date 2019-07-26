from playmaker.songs.models import Artist, Song, Genre

ARTIST_LIST = "artist_list"
ARTIST = "artist"
SONG_LIST = "song_list"
SONG = "song"
LIST = "_list"
TYPES = []


def get_cls(_t):
    if ARTIST in _t:
        cls = Artist
    elif SONG in _t:
        cls = Song
    else:
        raise Warning("Cannot find class: " + str(_t))

    return cls, LIST in _t


# TODO this should be a visitor (self method) on each obj. First section is artists, second is songs
def to_obj(cls, **_kwargs):
    kwargs = _kwargs.copy()
    if cls == Artist:
        kwargs["num_followers"] = kwargs.pop('followers').get('total')
        genre_names = kwargs.pop('genres')
        genres = [Genre.objects.get_or_create(name=g_n) for g_n in genre_names]
        kwargs["genres"] = genres

    elif cls == Song:
        kwargs = kwargs

    return cls(**kwargs)


def from_response(spotify_resp, type):
    cls, is_list = get_cls(type) # get the type (class) of object to cast the response into

    return [to_obj(cls, **i) for i in spotify_resp['items']] if is_list else cls(spotify_resp)