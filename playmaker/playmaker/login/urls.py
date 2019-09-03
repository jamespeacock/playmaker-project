from django.urls import path
from .views import SpotifyLoginView, SpotifyCallbackView

urlpatterns = [
    path('', SpotifyLoginView.as_view(), name="login-view"),
    path('get_auth', SpotifyCallbackView.as_view(), name="spotify-login-callback"),
]