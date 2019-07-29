from rest_framework import serializers
from playmaker.shared.serializers import ParamSerializer


class ActionSerializer(ParamSerializer):
    uris = serializers.CharField(allow_null=True, allow_blank=True)
    controller = serializers.CharField()


class QueueActionSerializer(ActionSerializer):
    action = serializers.CharField()