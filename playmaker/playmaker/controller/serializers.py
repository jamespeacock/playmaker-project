from rest_framework import serializers


class QueueActionSerializer(serializers.ModelSerializer):
    action = serializers.CharField()
    song_uri = serializers.CharField(allow_null=True, allow_blank=True)
