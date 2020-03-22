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
class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['name', 'type', 'is_active', 'sp_id']


class ListenerSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, required=False)
    active_device = DeviceSerializer(required=False)

    class Meta:
        model = Listener
        fields = ['group', 'devices', 'active_device']


class ControllerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Controller
        fields = ['group']
