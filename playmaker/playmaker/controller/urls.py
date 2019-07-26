from django.urls import path, include

from playmaker.controller.views import PlaySongView, QueueActionView

urlpatterns = [
    path('play', PlaySongView.as_view()),
    path('queue', QueueActionView.as_view())
]