from django.http import JsonResponse
from rest_framework import generics

from playmaker.controller import services
from playmaker.controller.contants import URIS, Q, SEARCH_TYPES, LIMIT, DEFAULT_Q_LIMIT, ALBUM
from playmaker.controller.models import Controller
from playmaker.shared.models import SPModel
from playmaker.shared.serializers import SearchSerializer, ParamSerializer
from playmaker.shared.utils import make_iterable
from playmaker.shared.views import SecureAPIView
from playmaker.controller.contants import ARTIST, TRACK
from playmaker.songs.models import Artist, Song, Album
from playmaker.songs.serializers import ArtistSerializer, SongSerializer, AlbumSerializer


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
        songs = services.fetch_songs(request.user.actor, make_iterable(params.get('uris')))
        return JsonResponse(services.as_views(songs, SongSerializer), status=200, safe=False)


class LoadArtistView(SecureAPIView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        uris = make_iterable(self.get_params(request.query_params).get(URIS))
        sp = request.user.sp
        for artist in SPModel.from_response(sp.artists(uris), Artist):
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
        cls, serializer = self.get_cls(_type)
        results = SPModel.from_response(results, cls, serializer=serializer, query=True)
        for i,r in enumerate(results['tracks']):
            r['position'] = i
        return JsonResponse(results, safe=False)

    def get_cls(self, _t):
        if ARTIST in _t:
            cls, ser = Artist, ArtistSerializer
        elif TRACK in _t:
            cls, ser = Song, SongSerializer
        elif ALBUM in _t:
            cls, ser = Album, AlbumSerializer
        else:
            raise Warning("Cannot find class: " + str(_t))

        return cls, ser