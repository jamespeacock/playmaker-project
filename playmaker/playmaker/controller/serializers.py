from rest_framework import serializers

from playmaker.controller.models import Device, Listener, Controller
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
class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['name', 'type', 'is_active', 'uri']


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

    # def create(self, validated_data):
    #     devices = validated_data.devices
    #     listener = validated_data.pop('listener')
    #     if listener:
    #         devices = [validated_data.active_device]
    #         return {'group': listener.group, 'devices': devices}
    #     controller = validated_data.pop('controller')
    #     if controller:
    #         return {'group': controller.group}
    #     return {}