from rest_framework import serializers

from playmaker.controller.models import Listener, Controller
from playmaker.shared.serializers import ParamSerializer
from playmaker.models import Device


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

    class Meta:
        model = Listener
        fields = ['group']


class ControllerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Controller
        fields = ['group']
