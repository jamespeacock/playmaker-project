from rest_framework import serializers
from rest_framework.serializers import Serializer


class StringListField(serializers.ListField):
    child = serializers.CharField()


class ParamSerializer(Serializer):
    uris = StringListField(allow_null=True, allow_empty=True, required=False)


class SearchSerializer(Serializer):
    q = serializers.CharField(allow_null=False, allow_blank=False)