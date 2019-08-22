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
def to_obj(__type, **_kwargs):
    cls, is_list = get_cls(__type)
    kwargs = _kwargs.copy()
    kwargs['sp_id'] = kwargs.pop('id')
    if cls == Artist:
        num_followers = kwargs.pop('followers').get('total')
        artist, a_created = Artist.objects.get_or_create(name=kwargs['name'], uri=kwargs['uri'], num_followers=num_followers)
        # genre_names = kwargs.pop('genres')
        # genres = [Genre.objects.get_or_create(name=g_n) for g_n in genre_names]
        # # kwargs["genres"] = genres
        return artist

    elif cls == Song:
        # TODO load as much as possible from a spotify song into Postgres.
        song, s_created = Song.objects.get_or_create(name=kwargs['name'], uri=kwargs['uri'], sp_id=kwargs['sp_id'])
        for artist in kwargs['artists']:
            artist['sp_id'] = artist.pop('id')
            a, a_created = Artist.objects.get_or_create(name=artist['name'], uri=artist['uri'], sp_id=artist['sp_id'])
            song.artists.add(a)

        return song

    # return cls(**kwargs)


def get_key(str_type):
    if str_type == SONG:
        return "tracks"


def from_response(spotify_resp, __type):
    # cls, is_list = get_cls(type) # get the type (class) of object to cast the response into

    response_data = spotify_resp[get_key(__type)]
    return [to_obj(__type, **i) for i in response_data if i]  # if is_list else [spotify_resp]


