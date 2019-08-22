from rest_framework import serializers
from playmaker.shared.serializers import ParamSerializer


class ActionSerializer(ParamSerializer):
    controller = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    listener = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class QueueActionSerializer(ActionSerializer):
    action = serializers.CharField(allow_null=True, allow_blank=True, required=False)