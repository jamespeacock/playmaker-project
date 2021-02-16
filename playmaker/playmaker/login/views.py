import cProfile
import logging
import pstats

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework.exceptions import ValidationError
from django.utils import timezone as tz
from social_django.utils import load_strategy

from api.settings import FRONTEND
from playmaker.controller.models import Controller
from playmaker.listener.models import Listener
from playmaker.controller.serializers import ControllerSerializer, ListenerSerializer
from playmaker.serializers import UserSerializer
from playmaker.shared.views import SecureAPIView

logger = logging.getLogger(__package__)


def is_authenticated(user):
    if user and hasattr(user, 'token') and len(user.token):
        return True
    else:
        return False


class IsLoggedInView(SecureAPIView):

    def get_serializer_class(self):
        return UserSerializer

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        super(IsLoggedInView, self).get(request)
        actor = {}
        user = request.user
        user.last_active = tz.now()
        user.save()
        u_actor = user.actor
        try:
            ser = None
            if type(u_actor) == Listener:
                ser = ListenerSerializer
            elif type(u_actor) == Controller:
                ser = ControllerSerializer
            if ser:
                actor = ser(u_actor).data
        except (Listener.DoesNotExist, Controller.DoesNotExist):
            pass

        ser = self.get_serializer_class()
        user_data = {**ser(user).data, 'actor': actor, 'is_logged_in': True, 'is_authenticated': is_authenticated(user)}

        return JsonResponse({'user': user_data})
