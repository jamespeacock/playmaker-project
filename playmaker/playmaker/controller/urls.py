from django.urls import path, include

from playmaker.controller.views import PlaySongView, PlaySongForAllListenersView

urlpatterns = [
    path('playsong', PlaySongView.as_view()),
    path('playsongall', PlaySongForAllListenersView.as_view())
]