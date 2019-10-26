from rest_framework import serializers

from playmaker.controller.models import Device, Listener
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


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ['group']

    def create(self, validated_data):
        listener = validated_data.pop('listener')
        if listener:
            return {'group': listener.group}
        controller = validated_data.pop('controller')
        if controller:
            return {'group': controller.group}
        return {}