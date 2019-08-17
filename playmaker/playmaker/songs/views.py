from django.http import JsonResponse
from rest_framework import generics

from playmaker.controller.models import Controller
from playmaker.shared.serializers import ParamSerializer
from playmaker.shared.utils import make_iterable
from playmaker.shared.views import SecureAPIView
from playmaker.songs.models import Song, Artist
from playmaker.songs.serializers import SongSerializer
from playmaker.songs.utils import from_response, SONG, ARTIST


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    # queryset = Song.objects.all()
    serializer_class = SongSerializer


class LoadSongView(SecureAPIView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        uris = make_iterable(self.get_params(request.GET).get('uris'))
        sp = Controller.objects.get(id=1).me.sp
        for song in from_response(sp.tracks(uris), SONG):
            to_save = Song(song)

        return JsonResponse({"status": "Done"})


class LoadArtistView(SecureAPIView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        uris = make_iterable(self.get_params(request.GET).get('uris'))
        sp = Controller.objects.get(id=1).me.sp
        for artist in from_response(sp.artists(uris), ARTIST):
            to_save = Artist(artist)
        pass


class SongDetailView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        pass