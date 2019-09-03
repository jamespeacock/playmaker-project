from rest_framework import serializers

from playmaker.controller.models import Device
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

