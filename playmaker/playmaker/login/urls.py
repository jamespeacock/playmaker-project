from django.urls import path
from .views import SpotifyLoginView, SpotifyCazllbackView

urlpatterns = [
    path('', SpotifyLoginView.as_view(), name="spotify-login"),
    path('get-auth', SpotifyCallbackView.as_view(), name="spotify-login-callback"),
]