from django.urls import path
from .views import SpotifyLoginView, SpotifyCallbackView, LogoutView, TestView

urlpatterns = [
    path('', SpotifyLoginView.as_view(), name="login-view"),
    path('get_auth', SpotifyCallbackView.as_view(), name="spotify-login-callback"),
    path('logout', LogoutView.as_view(), name="logout-view"),
    path('spotify-test', TestView.as_view(), name="spotify-test")
]