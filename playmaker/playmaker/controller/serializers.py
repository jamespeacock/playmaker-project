from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from playmaker.controller.models import Controller
from playmaker.listener.models import Listener
from playmaker.rooms.serializers import RoomSerializer
from playmaker.shared.serializers import ParamSerializer


# (Inbound)
# Parameter Serializers
class ActionSerializer(ParamSerializer):
    controller = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    listener = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class QueueActionSerializer(ActionSerializer):
    action = serializers.CharField(allow_null=True, allow_blank=True, required=False)


# (Outbound)
# Model Serializers
class ListenerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Listener
        fields = ['room', 'username']


class ControllerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    room = RoomSerializer(default={})

    class Meta:
        model = Controller
        fields = ['room', 'username']
