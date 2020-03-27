from django.http import JsonResponse
from rest_framework.generics import UpdateAPIView, ListAPIView

from playmaker.rooms.models import Room
from playmaker.rooms.serializers import RoomSerializer
from playmaker.shared.views import SecureAPIView


class RoomsListView(SecureAPIView, ListAPIView):

    def get(self, request, *args):
        return JsonResponse([RoomSerializer(d).data for d in Room.objects.all()], safe=False)


class RoomDetailView(UpdateAPIView, SecureAPIView):

    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get(self, request, room, *args):
        super(RoomDetailView, self).get(request, *args)
        return super(RoomDetailView, self).get(request, room, *args)
        # return JsonResponse(RoomSerializer(Room.objects.get(id=room)).data, safe=False)