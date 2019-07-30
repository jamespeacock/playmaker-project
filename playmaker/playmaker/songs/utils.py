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
    if cls == Artist:
        num_followers = kwargs.pop('followers').get('total')
        artist = Artist(name=kwargs['name'], uri=kwargs['uri'], num_followers=num_followers)
        # genre_names = kwargs.pop('genres')
        # genres = [Genre.objects.get_or_create(name=g_n) for g_n in genre_names]
        # # kwargs["genres"] = genres
        return artist

    elif cls == Song:
        song = Song(name=kwargs['name'], uri=kwargs['uri'])
        for artist in kwargs['artists']:
            if not Artist.objects.filter(name=artist['name']).first():
                a = Artist(name=artist['name'])
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