from django.urls import path

from playmaker.controller.views import PlaySongView, QueueActionView, NextSongView, SeekSongView, \
    StartRoomView, PollView, ModeDetailView

urlpatterns = [
    path('next', NextSongView.as_view()),
    path('mode', ModeDetailView.as_view()),
    path('play', PlaySongView.as_view()),
    path('queue/<str:action>', QueueActionView.as_view()),
    path('queue', QueueActionView.as_view()),
    path('seek', SeekSongView.as_view()),
    path('start', StartRoomView.as_view()),
    path('poll/<str:action>', PollView.as_view()),
]