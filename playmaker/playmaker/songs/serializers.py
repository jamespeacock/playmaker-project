from rest_framework import serializers

from playmaker.playlists.models import Playlist
from playmaker.songs.models import Song, Artist


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['name', 'uri']


class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['name', 'artists', 'uri']


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = SongSerializer(many=True, read_only=True)

    # TODO add playlist insights here and in model
    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'uri']