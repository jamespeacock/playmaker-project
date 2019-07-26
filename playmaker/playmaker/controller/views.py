from django.http import JsonResponse
from rest_framework import generics

# TODO implement internal session based &  token auth

from playmaker.controller import services
from playmaker.controller.serializers import ActionSerializer
from playmaker.shared.utils import make_iterable
from playmaker.controller.visitors import Action


LISTENERS = "listeners"
CONTROLLER = "controller"
URIS = "uris"


class SecureAPIView(generics.GenericAPIView):
    pass
    # grab Auth token from request header or auth user in request

    # ensure user making this action is the me of the controller_uuid specified


# Play song for current listeners

class PlaySongView(SecureAPIView):

    def get_param_serializer_class(self):
        return ActionSerializer

    def get_params(self, query_dict, serializer_cls=None):
        serializer_cls = serializer_cls or self.get_param_serializer_class()
        serializer = serializer_cls(data=query_dict)
        if serializer.is_valid(raise_exception=True):
            return serializer

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.GET)

        c = params.data.get(CONTROLLER)
        uris = params.data.get(URIS)
        failed_results = [r for r in services.perform_action(c, Action.PLAY, uris=make_iterable(uris)) if r]

        if failed_results:
            return JsonResponse(failed_results)

# Combine these with param action=
class QueueActionView(PlaySongView):

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

        services.perform_action(params.controller, params.listeners, params.action, params.uris)
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
