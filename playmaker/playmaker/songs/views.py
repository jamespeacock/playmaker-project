from rest_framework import generics
from playmaker.songs.models import Song
from playmaker.songs.serializers import SongSerializer


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongDetailView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        pass