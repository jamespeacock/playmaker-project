from rest_framework import serializers

from playmaker.playlists.models import Playlist
from playmaker.songs.models import Song, Artist, Album, Image


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['name', 'uri']


class ImageSerializer(serializers.ModelSerializer):
    height = serializers.IntegerField()
    width = serializers.IntegerField()
    url = serializers.CharField(max_length=512)

    class Meta:
        model = Image
        fields = ['height', 'width', 'url']


class AlbumSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Album
        fields = ['name', 'uri', 'images', 'artists']


class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    album = AlbumSerializer(many=False)

    class Meta:
        model = Song
        fields = ['name', 'artists', 'uri', 'album', 'position_ms', 'popularity', 'duration_ms']


class QueuedSongSerializer(SongSerializer):
    on_album = AlbumSerializer(many=False)
    in_q = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='position'
        )

    class Meta:
        model = Song
        fields = ['in_q', 'name', 'artists', 'uri', 'on_album', 'position_ms', 'popularity', 'duration_ms']


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = SongSerializer(many=True)

    # TODO add playlist insights here and in model
    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'uri']