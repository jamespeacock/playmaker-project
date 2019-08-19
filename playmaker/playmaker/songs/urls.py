from django.urls import path
from playmaker.songs.views import LoadSongView, LoadArtistView, SearchView


urlpatterns = [
    # path('songs/', ListSongsView.as_view(), name="songs-all")
    path('load_songs/', LoadSongView.as_view(), name="load-songs"),
    path('load_artists/', LoadArtistView.as_view(), name="load-artists"),
]
