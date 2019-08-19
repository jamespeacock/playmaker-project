from rest_framework import serializers
from rest_framework.serializers import Serializer


# class AttrDict(dict):
#
#     def __init__(self, data, *args, **kwargs):
#         super(AttrDict, self).__init__(data=data, *args, **kwargs)
#         self.__dict__ = self


class ParamSerializer(Serializer):
    uris = serializers.CharField(allow_null=True, allow_blank=True)


class SearchSerializer(Serializer):
    q = serializers.CharField(allow_null=False, allow_blank=False)