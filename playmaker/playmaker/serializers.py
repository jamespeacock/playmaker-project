from rest_framework import serializers

from playmaker.models import User, Device


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['name', 'type', 'is_active', 'sp_id']


class UserSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True)
    active_device = DeviceSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'sp_username', 'sp_id', 'is_controller', 'is_listener', 'active_device', 'devices')