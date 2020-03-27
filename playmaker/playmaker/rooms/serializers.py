from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from playmaker.rooms.models import Room
from playmaker.songs.serializers import SongSerializer


class RoomSerializer(serializers.ModelSerializer):
    listeners = SlugRelatedField(read_only=True, many=True, slug_field='username')
    controller = SlugRelatedField(read_only=True, slug_field='username')
    current_song = SongSerializer(read_only=True, default={}, required=False, allow_null=True)

    class Meta:
        model = Room
        fields = ['id', 'controller', 'listeners', 'current_song', 'name']