from rest_framework import serializers

from playmaker.playlists.models import Playlist
from playmaker.songs.models import Song, Artist, Album


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['name', 'uri']


class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    in_q = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='position'
    )

    class Meta:
        model = Song
        fields = ['name', 'artists', 'uri', 'in_q']


class AlbumSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    tracks = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = ['name', 'artists', 'tracks', 'uri']


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = SongSerializer(many=True)

    # TODO add playlist insights here and in model
    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'uri']