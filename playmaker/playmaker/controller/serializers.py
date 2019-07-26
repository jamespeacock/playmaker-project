from rest_framework import serializers
from playmaker.shared.serializers import ParamSerializer


class ActionSerializer(ParamSerializer):
    uris = serializers.CharField(allow_null=True, allow_blank=True)
    controller = serializers.CharField()
    listeners = serializers.ListField(serializers.CharField())

