import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView

from playmaker.controller.contants import DEVICE, URIS
from playmaker.controller.serializers import ListenerSerializer
from playmaker.controller.visitors import Action
from playmaker.listener.models import Listener
from playmaker.controller.models import Controller
from playmaker.rooms.models import Room
from playmaker.serializers import DeviceSerializer, UserSerializer
from playmaker.controller.services import stop_polling, get_queue, perform_action
from playmaker.listener.services import checkPlaySeek
from playmaker.shared.views import SecureAPIView

SP_USER = 'spotify:user:'


def find_room(room_identifier, return_all=False):

    # if room_indicator is spotify uri of friend
    if SP_USER in room_identifier:
        try:
            Room.objects.get(controller=Controller.objects.filter(me__sp_id=room_identifier))
        except Room.DoesNotExist as e:
            pass

    # if room_indicator is room_id
    try:
        rooms_match_by_name = Room.objects.filter(name=room_identifier).all()
        if rooms_match_by_name and return_all:
            return rooms_match_by_name
        elif rooms_match_by_name:
            return rooms_match_by_name.first()
        return Room.objects.get(id=room_identifier)
    except ValueError:
        return None


class StartListeningView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        super(StartListeningView, self).get(request)
        room_id = request.query_params.get('room')
        try:
            room = find_room(room_id) if room_id else None
        except Room.DoesNotExist:
            return JsonResponse("Room with indicator %s does not exist" % str(room_id), status=404, safe=False)

        try:
            user = request.user
            if getattr(user, 'controller', None):
                logging.log(logging.INFO, "Removing controller now that user wants to be a listener.")
                stop_polling(user)
                user.is_controller = False
                user.controller.delete()
            l = Listener.objects.filter(me=user).first()
            if not l:
                Listener.objects.get_or_create(me=user, room=room)
            else:
                l.room = room
                l.save()
            user.is_listener = True
            user.save()
        except IntegrityError as e:
            logging.log(logging.INFO, "Mismatch for user/room/listener")
            return JsonResponse("Mismatch for user/room/listener", safe=False)

        # TODO USE ListenerSerializer
        # Send back current queue, other listeners, etc.
        if user.actor:
            current_song = checkPlaySeek(user)
            response = {"room": {"id": room_id, "name": room.name},
                             "songs": []}
            if not current_song:
                response["error"] = "Device not found."
            else:
                response["currentSong"] = current_song
                response["queue"] = get_queue(user.actor)
            return JsonResponse(response)

        return JsonResponse({"error": "Listener object was not created."}, safe=False, status=500)


class LeaveRoomView(SecureAPIView):

    def get(self, request, *args):
        listener = request.user.listener
        listener.room = None
        listener.save()
        perform_action(None, Action.PAUSE, listeners=[listener])
        resp = ListenerSerializer(listener).data
        resp['room'] = resp['room'] or {}
        return JsonResponse(resp, safe=False)


class DevicesView(SecureAPIView, RetrieveAPIView):

    def get_serializer_class(self):
        return DeviceSerializer

    def get(self, request, *args, **kwargs):
        super(DevicesView, self).get(request)
        user = request.user
        devices = user.get_devices()

        return JsonResponse(UserSerializer(user).data, safe=False)

    def post(self, request, *args, **kwargs):
        super(DevicesView, self).post(request)
        user = request.user
        device_id = request.data.get(DEVICE)
        if user.set_device(device_id):
            current_song = checkPlaySeek(user, transfer=True)
            return JsonResponse({"user": UserSerializer(user).data, "current_song": current_song})
        return JsonResponse({"error": "Selected device %s was not found for requesting user." % device_id})


class ListenView(SecureAPIView, RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        currentSongView = request.user.actor.room.current_song(detail=True)
        return JsonResponse({"currentSong": currentSongView})


class SaveSongView(SecureAPIView):

    def post(self, request):
        uris = request.data.get(URIS)
        request.user.sp.current_user_saved_tracks_add(uris)

    def delete(self, request):
        uris = request.data.get(URIS)
        request.user.sp.current_user_saved_tracks_delete(uris)

# class GetQueueView(SecureAPIView, RetrieveAPIView):
#
#     def get(self, request, *args, **kwargs):
#         listener = request.user.listener
#         currentSong = checkPlaySeek(listener)
#         return JsonResponse({"currentSong": currentSong, "queue": listener.room.queue}, safe=False)