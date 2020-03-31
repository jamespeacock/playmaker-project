from django.urls import path

from playmaker.listener.views import StartListeningView, DevicesView, ListenView, LeaveRoomView

urlpatterns = [
    # path('queue', GetQueueView.as_view()),
    path('join', StartListeningView.as_view()),
    path('devices', DevicesView.as_view()),
    path('current', ListenView.as_view()),
    path('leave', LeaveRoomView.as_view())
]