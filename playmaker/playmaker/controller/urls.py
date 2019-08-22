from django.urls import path, include

from playmaker.controller.views import PlaySongView, QueueActionView, PauseSongView, NextSongView, SeekSongView, \
    StartListeningView

urlpatterns = [
    path('next', NextSongView.as_view()),
    path('pause', PauseSongView.as_view()),
    path('play', PlaySongView.as_view()),
    path('queue/<str:action>', QueueActionView.as_view()),
    path('queue', QueueActionView.as_view()),
    path('seek', SeekSongView.as_view()),
    path('start', StartListeningView.as_view()),
]