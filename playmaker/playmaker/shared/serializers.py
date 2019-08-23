from rest_framework import serializers
from rest_framework.serializers import Serializer


# class AttrDict(dict):
#
#     def __init__(self, data, *args, **kwargs):
#         super(AttrDict, self).__init__(data=data, *args, **kwargs)
#         self.__dict__ = self

class StringListField(serializers.ListField):
    child = serializers.CharField()


class ParamSerializer(Serializer):
    uris = StringListField(allow_null=True, allow_empty=True, required=False)


class SearchSerializer(Serializer):
    q = serializers.CharField(allow_null=False, allow_blank=False)