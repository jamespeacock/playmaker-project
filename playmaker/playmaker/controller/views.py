import asyncio
import logging

from rest_framework import generics, serializers
import spotipy


# TODO implement internal session based &  token auth
from rest_framework.serializers import IntegerField, ListField, CharField, Serializer

from playmaker.controller import utils
from playmaker.controller.models import Device
from playmaker.controller.serializers import QueueActionSerializer
from playmaker.controller.utils import START_PLAYBACK

from playmaker.models import User
from playmaker.controller.models import Controller, Listener

LISTENER = "listener"
CONTROLLER = "controller"
SONGS = "song_uris"


class SecureAPIView(generics.GenericAPIView):
    pass
    # grab Auth token from request header or auth user in request


# Play song for current listeners

class PlaySongView(SecureAPIView):

    def get(self, request, *args, **kwargs):

        listener = Listener.objects.get(id=request.GET.get(LISTENER))
        u = User.objects.get(id=listener.me.id)

        sp = spotipy.client.Spotify(auth=u.token)

        active_device_id = listener.devices.filter(is_active=True).first().sp_id

        sp.start_playback(active_device_id, uris=request.GET.getlist(SONGS))
        check = sp.current_playback()

        return check


class PlaySongForAllListenersView(PlaySongView):

    def get_param_serializer_class(self):
        pass

    def get(self, request, *args, **kwargs):
        # params = self.get_params(request.GET)
        controller = Controller.objects.get(id=request.GET.get(CONTROLLER))
        listeners = controller.listeners

        utils.perform_for_all(START_PLAYBACK, request.GET.get(LISTENER))


NEXT = 'next'
PLAY = 'play'
PAUSE = 'pause'
ADD = 'add'
CLEAR = 'clear'


# Combine these with param action=
class QueueActionView(SecureAPIView):

    def get_param_serializer_class(self):
        return QueueActionSerializer

    def get_params(self, query_dict, serializer_cls=None):
        serializer_cls = serializer_cls or self.get_param_serializer_class()
        serializer = serializer_cls(data=query_dict)
        if serializer.is_valid(raise_exception=True):
            return serializer

    """
    Returns current list of songs in queue.
    """
    def get(self, request, *args, **kwargs):
        pass

    """
    Performs specified action on current queue for current room/group/controller.
    @:param action - string: action to perform
        - Valid actions are: next/play/pause/add/clear
    """
    def post(self, request, *args, **kwargs):
        params = self.get_params(request.POST)
        # return self.render(params)



# Seek to section of users current song


# Shuffle


# Get devices / Transfer playback
#?

### Listener/Group Data Section

class GroupTastesView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        pass
