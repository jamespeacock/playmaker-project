from django.urls import path

from playmaker.controller.views import QueueActionView
from playmaker.listener.views import StartListeningView, DevicesView

urlpatterns = [
    path('queue', QueueActionView.as_view()),
    path('join', StartListeningView.as_view()),
    path('devices', DevicesView.as_view()),
]