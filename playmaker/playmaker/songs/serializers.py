from rest_framework import serializers
from playmaker.songs.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
