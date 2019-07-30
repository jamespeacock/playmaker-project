from rest_framework import generics

from playmaker.shared.serializers import ParamSerializer


class SecureAPIView(generics.GenericAPIView):
    # grab Auth token from request header or auth user in request
    # ensure user making this action is the me of the controller_uuid specified
    def get_param_serializer_class(self):
        return ParamSerializer

    def get_params(self, query_dict, serializer_cls=None):
        serializer_cls = serializer_cls or self.get_param_serializer_class()
        serializer = serializer_cls(data=query_dict)
        if serializer.is_valid(raise_exception=True):
            return serializer.data