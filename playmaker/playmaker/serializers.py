from rest_framework import serializers

from playmaker.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'sp_username', 'sp_id', 'is_controller', 'is_listener')