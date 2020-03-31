from django.utils import timezone as tz
from rest_framework import generics

from playmaker.models import User
from playmaker.shared.serializers import ParamSerializer
from playmaker.shared.utils import NotLoggedInException


class SecureAPIView(generics.GenericAPIView):
    # grab Auth token from request header or auth user in request
    # ensure user making this action is the me of the controller_uuid specified - done in services
    def get_param_serializer_class(self):
        return ParamSerializer

    def get_params(self, query_dict, serializer_cls=None):
        serializer_cls = serializer_cls or self.get_param_serializer_class()
        serializer = serializer_cls(data=query_dict)
        if serializer.is_valid(raise_exception=False):
            return serializer.data
        return {}

    def get(self, request, *args, **kwargs):
        # This check if only true if the user has a valid token and is therefore not an AnonymousUser
        user = request.user
        if not isinstance(user, User):
            raise NotLoggedInException
        user.last_active = tz.now()
        user.save() #How expensive is this ?  Will later calls to save handle it

    def post(self, request, *args, **kwargs):
        # This check if only true if the user has a valid token and is therefore not an AnonymousUser
        user = request.user
        if not isinstance(user, User):
            raise NotLoggedInException
        user.last_action = tz.now()
        user.save()