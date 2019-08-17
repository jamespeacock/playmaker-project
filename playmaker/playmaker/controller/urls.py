from django.urls import path, include

from playmaker.controller.views import PlaySongView, QueueActionView, PauseSongView, NextSongView, SeekSongView, \
    StartListeningView

urlpatterns = [
    path('start', StartListeningView.as_view()),
    path('play', PlaySongView.as_view()),
    path('queue', QueueActionView.as_view()),
    path('pause', PauseSongView.as_view()),
    path('next', NextSongView.as_view()),
    path('seek', SeekSongView.as_view()),
]