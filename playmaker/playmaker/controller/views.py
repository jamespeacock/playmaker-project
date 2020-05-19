import logging
from django.http import JsonResponse
from playmaker.controller import services
from playmaker.controller.contants import URIS, ADD, REMOVE, START, STOP
from playmaker.listener.models import Listener
from playmaker.controller.serializers import QueueActionSerializer
from playmaker.controller.services import start_polling, stop_polling, create_controller_and_room, \
    perform_action_for_listeners, perform_action
from playmaker.controller.visitors import Action
from playmaker.listener.services import checkPlaySeek
from playmaker.models import User
from playmaker.rooms.services import next_in_queue, add_to_queue, remove_from_queue, get_queue
from playmaker.shared.views import SecureAPIView


class ControllerView(SecureAPIView):

    def get(self, request):
        super(ControllerView, self).get(request)
        # Leaving this instead of deleting it in case it does become required to pass in controller ID for action
        # instead of just looking it up via user.
        # if not services.user_matches_actor(request.user, request.query_params.get(CONTROLLER), Controller):
        #     return JsonResponse("You cannot perform this action for controller specified.", status=401, safe=False)


# Create a group
class StartRoomView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        super(StartRoomView, self).get(request)
        user = request.user
        if getattr(user, 'listener', None):
            logging.log(logging.INFO, "Removing listener now that user wants to be controller.")
            Listener.objects.get(me=user).delete()
        mode = request.GET.get('mode', '')
        room_id, controller_id = create_controller_and_room(user, mode)

        if not user.hasActivePoller:
            start_polling(user)
        current_song = User.objects.get(username=user.username).actor.queue.now_playing() if mode != 'curate' else {}
        return JsonResponse({"room": {"id": room_id}, "controller": controller_id, "currentSong": current_song or {}})


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
        user = request.user
        actor = user.actor
        next_song = next_in_queue(actor.queue)
        if next_song:
            user.play_song(next_song)
            success = perform_action_for_listeners(actor, Action.PLAY, uris=[next_song])
            success = stop_polling(user) and success
            success = start_polling(user) and success
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
        songs = get_queue(actor)
        current_song = checkPlaySeek(user) # Redundant check to make sure song showing up on UI is actually playing too.
        if current_song:
            return JsonResponse({"currentSong": current_song, "queue": songs}, safe=False)
        if user.is_listener and actor and user.active_device:
            perform_action(None, Action.PAUSE, listeners=[actor])
        return JsonResponse({"error": "There is a problem with the queue/group. Most likely it has been closed or user have left it."},
                            status=404, safe=False)

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
            success = add_to_queue(user.uuid, body.get(URIS))
        elif action == REMOVE:
            success = remove_from_queue(user.uuid, body.get(URIS), body.get('positions'))

        songs = get_queue(actor)
        current_song = actor.queue.now_playing()
        return JsonResponse({"success": success, "currentSong": current_song, "queue": songs}, safe=False)


class PollView(ControllerView):

    #TODO have frontend periodically ensure this is still running
    def get(self, request, action=None, *args, **kwargs):
        super(PollView, self).get(request)
        try:
            user = request.user
            if action == START:
                started = start_polling(user)
                return JsonResponse({"started": started})
            elif action == STOP:
                stopped = stop_polling(user)
                return JsonResponse({"stopped": stopped})
        except Exception as e:
            logging.log(logging.ERROR, e)
            return JsonResponse(str(e), status=500, safe=False)


class CloseRoomView(ControllerView):

    def get(self, request, *args):
        actor = request.user.controller
        success = perform_action_for_listeners(actor, Action.PAUSE)
        print("Closed room: " + str(success))
        print(actor.delete())
        request.user.save()
        return JsonResponse({})


class ModeDetailView(ControllerView):

    def put(self, request, ):
        pass

# Fetch Playlists

# Fetch Recommendations

#  - filter recs


