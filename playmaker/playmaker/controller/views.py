import asyncio
import logging

from rest_framework import generics, serializers
import spotipy


# TODO implement internal session based &  token auth
from rest_framework.serializers import IntegerField, ListField, CharField, Serializer

from playmaker.controller import utils
from playmaker.controller.models import Device
from playmaker.controller.utils import START_PLAYBACK

from playmaker.models import User
from controller.models import Controller, Listener

LISTENER = "listener"
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

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.GET)
        controller = Controller.objects.get(id=params.controller)
        listeners = controller.listeners

        utils.perform_for_all(START_PLAYBACK, params.listener)


# Add a song to users queue


# Seek to section of users current song


# Shuffle

# Next Track / Prev track

# Get devices / Transfer playback
