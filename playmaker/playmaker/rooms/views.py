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

    def get(self, request, pk, *args):
        super(RoomDetailView, self).get(request, pk, *args)
        # return super(RoomDetailView, self).get(request, room, *args)
        room_obj = Room.objects.filter(id=pk).first()
        if room_obj:
            return JsonResponse(RoomSerializer(room_obj).data, safe=False)
        else:
            return JsonResponse({"error": "Room with id %s does not exist." % str(pk)}, status=404)