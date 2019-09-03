from playmaker.shared.models import SPModel
from playmaker.songs.models import Song
from playmaker.songs.serializers import SongSerializer


# Fetch and save songs


def fetch_songs(actor, uris, save=False):
    if uris:
        sp = actor.me.sp
        return SPModel.from_response(sp.tracks(uris), Song, serializer=SongSerializer, save=save)
    return []
