from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView

from playmaker.controller.models import Listener, Group, Controller
from playmaker.controller.serializers import DeviceSerializer
from playmaker.shared.views import SecureAPIView

SP_USER = 'spotify:user:'


def find_group(group_identifier):

    # if group_indicator is spotify uri of friend
    if SP_USER in group_identifier:
        try:
            Group.objects.get(controller = Controller.objects.filter(me__sp_id=group_indicator))
        except ObjectDoesNotExist as e:
            pass

    # if group_indicator is group_id
    try:
        return Group.objects.get(id=group_identifier)
    except ObjectDoesNotExist as e:
        return None


class StartListeningView(SecureAPIView):

    def get(self, request, *args, **kwargs):
        group_id = request.query_params.get('group')

        group = find_group(group_id)
        if not group:
            return JsonResponse("Group with indicator %s des not exist" % str(group_id), safe=False)

        listener, created = Listener.objects.get_or_create(me=request.user, group=group)
        listener.refresh()

        return JsonResponse({"listener": listener.me.uuid})


class DevicesView(SecureAPIView, RetrieveAPIView):

    def get_serializer_class(self):
        return DeviceSerializer

    def get(self, request, *args, **kwargs):
        actor = request.user.actor
        ser = self.get_serializer_class()
        if not actor.devices.first():
            actor.refresh()
        print(len(actor.devices.all()))
        return JsonResponse([ser(d).data for d in actor.devices.all()], safe=False)

