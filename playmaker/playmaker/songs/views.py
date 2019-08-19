from django.http import JsonResponse
from rest_framework import generics

from playmaker.controller.contants import URIS, Q, SEARCH_TYPES
from playmaker.controller.models import Controller
from playmaker.shared.serializers import SearchSerializer
from playmaker.shared.utils import make_iterable
from playmaker.shared.views import SecureAPIView
from playmaker.songs.models import Song, Artist
from playmaker.songs.serializers import SongSerializer
from playmaker.songs.services import to_view
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
        controller = Controller.objects.get(id=1)
        sp = controller.me.sp
        for song in from_response(sp.tracks(uris), SONG):
            to_save = Song(song)
            controller.queue.add(to_save)

        return JsonResponse({"status": "Done"})


class LoadArtistView(SecureAPIView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        uris = make_iterable(self.get_params(request.query_params).get(URIS))
        sp = Controller.objects.get(id=1).me.sp
        for artist in from_response(sp.artists(uris), ARTIST):
            to_save = Artist(artist)
        pass


class SongDetailView(SecureAPIView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        pass


class SearchView(SecureAPIView, generics.RetrieveAPIView):

    def get_param_serializer_class(self):
        return SearchSerializer

    def get(self, request, _type, *args, **kwargs):
        sp = request.user.sp
        params = self.get_params(request.query_params)
        assert _type in SEARCH_TYPES
        results = sp.search(params.get(Q),
                            type=_type,
                            limit=params.get('limit', 10))
        return JsonResponse(to_view(results, _type), safe=False)
