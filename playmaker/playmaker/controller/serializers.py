from rest_framework import serializers
from playmaker.shared.serializers import ParamSerializer


class ActionSerializer(ParamSerializer):
    controller = serializers.CharField()


class QueueActionSerializer(ActionSerializer):
    action = serializers.CharField()