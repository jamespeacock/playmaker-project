import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView

from playmaker.controller.contants import DEVICE
from playmaker.controller.models import Listener, Group, Controller
from playmaker.serializers import DeviceSerializer, UserSerializer
from playmaker.controller.services import stop_polling
from playmaker.listener.services import checkPlaySeek
from playmaker.shared.views import SecureAPIView

SP_USER = 'spotify:user:'


def find_group(group_identifier):

    # if group_indicator is spotify uri of friend
    if SP_USER in group_identifier:
        try:
            Group.objects.get(controller=Controller.objects.filter(me__sp_id=group_identifier))
        except ObjectDoesNotExist as e:
            pass

    # if group_indicator is group_id
    try:
        return Group.objects.get(id=group_identifier)
    except ObjectDoesNotExist as e:
        return None
    except ValueError:
        return None


class StartListeningView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        super(StartListeningView, self).get(request)
        group_id = request.query_params.get('group')
        group = find_group(group_id)
        if not group:
            return JsonResponse("Group with indicator %s does not exist" % str(group_id), status=404, safe=False)

        try:
            user = request.user
            Listener.objects.get_or_create(me=user, group=group)
            if getattr(user, 'controller', None):
                logging.log(logging.INFO, "Removing controller now that user wants to be a listener.")
                stop_polling(user)
                Controller.objects.get(me=user).delete()
        except IntegrityError as e:
            logging.log(logging.INFO, "Mismatch for user/group/listener")
            return JsonResponse("Mismatch for user/group/listener", safe=False)

        # TODO return group/session info
        # Send back current queue, other listeners, etc.
        return JsonResponse({"group": group_id,
                             "songs": [],
                             "currentSong": group.current_song(detail=True)
                             })


class DevicesView(SecureAPIView, RetrieveAPIView):

    def get_serializer_class(self):
        return DeviceSerializer

    def get(self, request, *args, **kwargs):
        super(DevicesView, self).get(request)
        user = request.user
        ser = self.get_serializer_class()

        return JsonResponse(UserSerializer(user).data, safe=False)

    def post(self, request, *args, **kwargs):
        super(DevicesView, self).post(request)
        user = request.user
        device_id = request.data.get(DEVICE)
        if user.set_device(device_id):
            current_song = checkPlaySeek(user)
            return JsonResponse({"user": UserSerializer(user).data, "current_song": current_song})
        return JsonResponse({"error": "Selected device %s was not found for requesting user." % device_id})


class ListenView(SecureAPIView, RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        currentSongView = request.user.actor.group.current_song(detail=True)
        return JsonResponse({"currentSong": currentSongView})


# class GetQueueView(SecureAPIView, RetrieveAPIView):
#
#     def get(self, request, *args, **kwargs):
#         listener = request.user.listener
#         currentSong = checkPlaySeek(listener)
#         return JsonResponse({"currentSong": currentSong, "queue": listener.group.queue}, safe=False)