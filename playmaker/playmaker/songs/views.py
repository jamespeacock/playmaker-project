from django.http import JsonResponse
from rest_framework import generics

from playmaker.controller import services
from playmaker.controller.contants import URIS, Q, SEARCH_TYPES, LIMIT, DEFAULT_Q_LIMIT, CONTROLLER
from playmaker.controller.models import Controller
from playmaker.shared.serializers import SearchSerializer, ParamSerializer
from playmaker.shared.utils import make_iterable
from playmaker.shared.views import SecureAPIView
from playmaker.songs.models import Artist
from playmaker.songs.serializers import SongSerializer
from playmaker.songs.utils import from_response, ARTIST


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    # queryset = Song.objects.all()
    serializer_class = SongSerializer


class LoadSongView(SecureAPIView, generics.RetrieveAPIView):

    def get_param_serializer_class(self):
        return ParamSerializer

    def get(self, request, *args, **kwargs):
        params = self.get_params(request.query_params)
        uris = make_iterable(params.get('uris'))
        songs = services.fetch_songs(request.user.actor, make_iterable(uris))
        return JsonResponse(services.as_views(songs, SongSerializer), status=200, safe=False)


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
        q = params.get(Q, None)
        assert _type in SEARCH_TYPES
        if not q:
            return JsonResponse([], safe=False)
        results = sp.search(q,
                            type=_type,
                            limit=params.get(LIMIT, DEFAULT_Q_LIMIT))
        return JsonResponse(from_response(results, _type), safe=False)
