import logging
from collections import defaultdict
from django.http import JsonResponse
from playmaker.controller import services
from playmaker.controller.contants import URIS, ADD, REMOVE, URI, START, STOP
from playmaker.controller.models import Controller, Group, Queue, Listener
from playmaker.controller.serializers import QueueActionSerializer
from playmaker.controller.services import next_in_queue, start_polling, stop_polling
from playmaker.shared.utils import make_iterable
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
        if getattr(request.user, 'listener', None):
            logging.log(logging.INFO, "Removing listener now that user wants to be controller.")
            Listener.objects.get(me=request.user).delete()
        controller, created = Controller.objects.get_or_create(me=request.user)
        Queue.objects.get_or_create(controller=controller)
        group, created = Group.objects.get_or_create(controller=controller)
        if not created:
            logging.log(logging.INFO, "Group was not created for some reason!")

        started = start_polling(request.user)
        return JsonResponse({"group": group.id, "controller": controller.id, "started": started})


# Play song for current listeners

class PlaySongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(PlaySongView, self).get(request)
        params = self.get_params(request.query_params)

        if not params.get(URIS):
            return

        failed_results = [r for r in services.perform_action(
            request.user,
            Action.PLAY,
            uris=make_iterable(params.get(URIS))) if r]

        if failed_results:
            return JsonResponse({"status": []})

        return JsonResponse({"status": "Success."})


class PauseSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(PauseSongView, self).get(request)
        failed_results = [r for r in services.perform_action(
            request.user,
            Action.PAUSE) if r]

        if failed_results:
            return JsonResponse({"status": "Meh."})

        return JsonResponse({"status": "Success."})


class NextSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        super(NextSongView, self).get(request)
        next_song = next_in_queue(request.user.actor.queue)
        if next_song:
            failed_results = [r for r in services.perform_action(
                request.user,
                Action.PLAY,
                uris=[next_song.uri]) if r]
        else:
            return JsonResponse("No songs remain in the queue.", safe=False)

        if failed_results:
            return JsonResponse({"status": failed_results})

        return JsonResponse({"status": "Success."})


class SeekSongView(ControllerView):

    def get(self, request, *args, **kwargs):
        not_authed_resp = super(SeekSongView, self).get(request)
        if not_authed_resp:
            return not_authed_resp
        pos = request.query_params.get('position', None)
        if pos:
            failed_results = [r for r in services.perform_action(
                request.user,
                Action.SEEK,
                position_ms=pos) if r]

            if failed_results:
                return JsonResponse({"status": failed_results})

        return JsonResponse({"status": "Success."})


class QueueActionView(ControllerView):

    def get_param_serializer_class(self):
        return QueueActionSerializer

    """
    Returns current list of songs in queue.
    """
    def get(self, request, *args, **kwargs):
        super(QueueActionView, self).get(request)
        params = request.query_params
        songs = services.get_queue(params, request.user)
        # post filter songs to make sure each song has just one position
        seen = defaultdict(int)
        for s in songs:
            s['position'] = s.pop('in_q')[seen[s[URI]]]
            seen[s[URI]] += 1

        return JsonResponse(songs, safe=False)

    """
    Performs specified action on current queue for current room/group/controller.
    @:param action - string: action to perform
    """
    def post(self, request, action=None, *args, **kwargs):
        # TODO how to validate contents of request body
        super(QueueActionView, self).post(request)
        body = request.data
        if action == ADD:
            res = services.add_to_queue(request.user.uuid, body.get(URIS))
        elif action == REMOVE:
            res = services.remove_from_queue(request.user.uuid, body.get(URIS), body.get('positions'))

        return JsonResponse({"success": res}, status=200, safe=False) if res else\
            JsonResponse("That action could not be completed.", status=500, safe=False)


class PollView(ControllerView):

    def get(self, request, action=None, *args, **kwargs):
        super(PollView, self).get(request)
        try:
            if action == START:
                # kicks off thread that will poll until song changes and then
                started = start_polling(request.user)
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
