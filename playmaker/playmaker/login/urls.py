from django.urls import path
from .views import SpotifyLoginView

urlpatterns = [
    path('', SpotifyLoginView.as_view(), name="spotify-login")
]