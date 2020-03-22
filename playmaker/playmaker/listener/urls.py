from django.urls import path

from playmaker.listener.views import StartListeningView, DevicesView, ListenView

urlpatterns = [
    # path('queue', GetQueueView.as_view()),
    path('join', StartListeningView.as_view()),
    path('devices', DevicesView.as_view()),
    path('current', ListenView.as_view()),
]