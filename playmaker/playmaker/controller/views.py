import logging
from django.http import JsonResponse
from playmaker.controller import services
from playmaker.controller.contants import URIS, ADD, REMOVE, START, STOP
from playmaker.controller.models import Listener
from playmaker.controller.serializers import QueueActionSerializer
from playmaker.controller.services import next_in_queue, start_polling, stop_polling, create_controller_and_group, \
    perform_action_for_listeners
from playmaker.listener.services import checkPlaySeek
from playmaker.controller.visitors import Action
from playmaker.shared.views import SecureAPIView


class ControllerView(SecureAPIView):

    def get(self, request):
        super(ControllerView, self).get(request)
        # Leaving this instead of deleting it in case it does become required to pass in controller ID for action
        # instead of just looking it up via user.
        # if not services.user_matches_actor(request.user, request.query_params.get(CONTROLLER), Controller):
        #     return JsonResponse("You cannot perform this action for controller specified.", status=401, safe=False)


# Create a group
class StartGroupView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        super(StartGroupView, self).get(request)
        user = request.user
        if getattr(user, 'listener', None):
            logging.log(logging.INFO, "Removing listener now that user wants to be controller.")
            Listener.objects.get(me=user).delete()
        mode = request.GET.get('mode', '')
        group_id, controller_id = create_controller_and_group(user, mode)

        start_polling(user)
        currentSong = user.actor.queue.currently_playing(detail=True, refresh=True) if mode == 'broadcast' else {}
        return JsonResponse({"group": group_id, "controller": controller_id, "currentSong": currentSong})


# Play song for current listeners

class PlaySongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(PlaySongView, self).get(request)
        params = self.get_params(request.query_params)

        if not params.get(URIS):
            return JsonResponse({"error": "Did not provide URIs to play."})
        actor = request.user.actor
        success = perform_action_for_listeners(actor, Action.PLAY, uris=params.get(URIS))

        return JsonResponse({"status": success})


class NextSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(NextSongView, self).get(request)
        actor = request.user.actor
        next_song = next_in_queue(actor.queue)
        if next_song:
            success = perform_action_for_listeners(actor, Action.PLAY, uris=[next_song])
        else:
            songs = actor.group.suggest_next_songs()
            return JsonResponse({"suggested": songs, "success": False}, safe=False)

        return JsonResponse({"status": success})


class SeekSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(SeekSongView, self).get(request)
        pos = request.query_params.get('position', None)
        if pos:
            actor = request.user.actor
            success = perform_action_for_listeners(actor, Action.SEEK, position_ms=pos)
            return JsonResponse({"status": success})
        return JsonResponse({"error": "Missing 'position' parameter."})


class QueueActionView(ControllerView):

    def get_param_serializer_class(self):
        return QueueActionSerializer

    """
    Returns current list of songs in queue.
    """
    def get(self, request, *args, **kwargs):
        super(QueueActionView, self).get(request)
        user = request.user
        actor = user.actor
        songs = services.get_queue(actor)
        current_song = checkPlaySeek(user)
        return JsonResponse({"currentSong": current_song, "queue": songs}, safe=False)

    """
    Performs specified action on current queue for current room/group/controller.
    @:param action - string: action to perform
    """
    def post(self, request, action=None, *args, **kwargs):
        # TODO how to validate contents of request body
        super(QueueActionView, self).post(request)
        body = request.data
        user = request.user
        actor = user.actor
        if action == ADD:
            success = services.add_to_queue(user.uuid, body.get(URIS))
        elif action == REMOVE:
            success = services.remove_from_queue(user.uuid, body.get(URIS), body.get('positions'))

        songs = services.get_queue(actor)
        current_song = actor.queue.currently_playing()
        return JsonResponse({"success": success, "currentSong": current_song, "queue": songs}, safe=False)


class PollView(ControllerView):

    #TODO have frontend periodically ensure this is still running
    def get(self, request, action=None, *args, **kwargs):
        super(PollView, self).get(request)
        try:
            if action == START:
                # kicks off thread that will poll until song changes and then
                user = request.user
                user.shouldPoll = True
                # user.save()
                started = start_polling(user)
                return JsonResponse({"started": started})
            elif action == STOP:
                stopped = stop_polling()
                return JsonResponse({"stopped": stopped})
        except Exception as e:
            logging.log(logging.ERROR, e)
            return JsonResponse(str(e), status=500, safe=False)


# Listener/Group Data Section
class GroupTastesView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        pass

# Fetch Playlists

# Fetch Recommendations

#  - filter recs
