from django.urls import path

from playmaker.rooms.views import RoomsListView, RoomDetailView

urlpatterns = [
    path('all', RoomsListView.as_view()),
    path('<int:pk>', RoomDetailView.as_view())
]