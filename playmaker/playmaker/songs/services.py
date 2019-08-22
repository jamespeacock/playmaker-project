from playmaker.controller.contants import TRACK, ARTIST
from playmaker.songs.models import Song
from playmaker.songs.utils import SONG, from_response


def to_view(data, _type):

    m = { TRACK: to_song_view,
          ARTIST: to_artist_view}

    view = m[_type]

    items = data.get(_type+'s').get('items')

    return [view(i) for i in items]


def to_song_view(song):
    return {'name': song.get('name'),
            'uri': song.get('uri'),
            'artists': song.get('artists')}
            # 'artists': ','.join([a.get('name') for a in song.get('artists')])}


def to_artist_view(artist):
    return {'name': artist.get('name'),
            'uri': artist.get('uri')}


def to_playlist_view(playlist):
    pass


# Fetch and save songs
def fetch_songs(actor, uris):
    if uris:
        sp = actor.me.sp
        return from_response(sp.tracks(uris), SONG)
    return []
