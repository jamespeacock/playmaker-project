from rest_framework import serializers

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


