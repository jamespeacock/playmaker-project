from playmaker.controller.contants import TRACK, ARTIST


def to_view(data, _type):

    m = { TRACK: to_song_view,
          ARTIST: to_artist_view}

    view = m[_type]

    items = data.get(_type+'s').get('items')

    return [view(i) for i in items]


def to_song_view(song):
    return {'name': song.get('name'),
            'uri': song.get('uri'),
            'artists': ','.join([a.get('name') for a in song.get('artists')])}


def to_artist_view(artist):
    return {'name': artist.get('name'),
            'uri': artist.get('uri')}


def to_playlist_view(playlist):
    pass