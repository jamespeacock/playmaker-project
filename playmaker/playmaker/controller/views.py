import logging

from rest_framework import generics, serializers
import spotipy


# TODO implement internal session based &  token auth
from rest_framework.serializers import IntegerField, ListField, CharField, Serializer

from playmaker.controller import utils
from playmaker.controller.models import Device
from playmaker.controller.utils import START_PLAYBACK

from playmaker.models import User, Listener, Controller


LISTENER = "listener"
SONGS = "song_uris"

class SecureAPIView(generics.GenericAPIView):
    pass
    # grab Auth token from request header or auth user in request


# TODO figure out a shared method that executes an action for a bunch of users. ex: all users need a song queued

class StringListField(ListField):
    child = CharField()
# Play song for current listeners

class PlaySongView(SecureAPIView):

    def get(self, request, *args, **kwargs):

        listener = Listener.objects.get(id=request.GET.get(LISTENER))
        u = User.objects.get(id=listener.me.id)

        sp = spotipy.client.Spotify(auth=u.token)

        #TODO extract device fetch process to be reused
        devices = []
        for d in sp._get('me/player/devices')['devices']:
            d['sp_id'] = d.pop('id')
            dev = Device(**d)
            dev.save()
            devices.append(dev)

        listener.devices.set(devices)
        active_device_id = listener.devices.filter(is_active=True).first().sp_id

        # VERIFY ACTION PERMISSION object

        r = sp._put('me/player/play?device_id='+active_device_id, payload={'uris': request.GET.getlist(SONGS)})

        check = sp._get('me/player')

        return r

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
