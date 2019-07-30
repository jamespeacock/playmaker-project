from django.http import JsonResponse
from rest_framework import generics

# TODO implement internal session based &  token auth

from playmaker.controller import services
from playmaker.controller.models import Controller
from playmaker.controller.serializers import ActionSerializer, QueueActionSerializer
from playmaker.shared.utils import make_iterable
from playmaker.controller.visitors import Action
from playmaker.shared.views import SecureAPIView

LISTENERS = "listeners"
CONTROLLER = "controller"
URIS = "uris"

# Queue action
ACTION = "action"


class ControllerView(SecureAPIView):
    pass
    # def get_param_serializer_class(self):
    #     return ActionSerializer
    #
    # def get_params(self, query_dict, serializer_cls=None):
    #     serializer_cls = serializer_cls or self.get_param_serializer_class()
    #     serializer = serializer_cls(data=query_dict)
    #     if serializer.is_valid(raise_exception=True):
    #         return serializer.data


# Play song for current listeners

class PlaySongView(ControllerView):

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.GET)

        failed_results = [r for r in services.perform_action(
            1,  # params.get(CONTROLLER),
            Action.PLAY,
            uris=make_iterable(params.get(URIS))) if r]

        if failed_results:
            return JsonResponse({"status": "Meh."})

        return JsonResponse({"status": "Success."})


class PauseSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.GET)

        failed_results = [r for r in services.perform_action(
            1, #params.get(CONTROLLER),
            Action.PAUSE) if r]

        if failed_results:
            return JsonResponse({"status": "Meh."})

        return JsonResponse({"status": "Success."})


class NextSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.GET)

        # TODO decide if this should pick next song from internal queue and press play
        #  or skip to next song in each listener's queue
        c = 1  # params.get(CONTROLLER)
        failed_results = [r for r in services.perform_action(
            c,
            Action.NEXT,
            uris=services.get_next_song(c)) if r]

        if failed_results:
            return JsonResponse({"status": "Meh."})

        return JsonResponse({"status": "Success."})


class SeekSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        c = 1  # params.get(CONTROLLER)
        failed_results = [r for r in services.perform_action(
            c,
            Action.SEEK,
            position_ms=35000) if r]

        if failed_results:
            return JsonResponse({"status": "Meh."})

        return JsonResponse({"status": "Success."})


class QueueActionView(ControllerView):

    def get_param_serializer_class(self):
        return QueueActionSerializer

    """
    Returns current list of songs in queue.
    """
    def get(self, request, *args, **kwargs):
        c = 1
        cont = Controller.objects.get(id=c)
        songs = []
        for song in cont.queue.songs.all():
            songs.append({"name": song.name, "artists": [a.name for a in song.artists]})

        return JsonResponse({"status": "Meh."})


    """
    Performs specified action on current queue for current room/group/controller.
    @:param action - string: action to perform
    """
    def post(self, request, *args, **kwargs):
        params = self.get_params(request.POST)


        services.perform_action(params.get(CONTROLLER), params.get(ACTION), params.get(URIS))
        return self.render(params)

# Seek to section of users current song
# Queue Song, Play Song @ timestamp?

# Fetch Playlists

# Fetch Recommendations
#  - filter recs

# Add Song to Playlist

# Save Song

# HOW TO Crossfade into other songs?

# Shuffle


# Get devices / Transfer playback
#?

### Listener/Group Data Section

class GroupTastesView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        pass
