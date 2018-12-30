from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
import spotipy as sp
import logging


# Create your views here.
class SpotifyLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        logging.log(logging.INFO, "In spotify login GET")
        return HttpResponse(status=200)