import json
import logging

import six.moves.urllib.parse as urllibparse
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from playmaker.login import services
from playmaker.models import User


class SpotifyLoginView(LoginView):

    def get_redirect(self, username):
        logging.log(logging.INFO, "In spotify login GET %s" % username)

        url = 'https://accounts.spotify.com/authorize'
        print(SPOTIFY_REDIRECT_URI)
        urlparams = urllibparse.urlencode({'client_id': SPOTIFY_CLIENT_ID, 'response_type': 'code',
                                           'redirect_uri': SPOTIFY_REDIRECT_URI, 'scope': SPOTIFY_SCOPE,
                                           'state': 'username-' + username})

        redirect_url = '%s?%s' % (url, urlparams)
        logging.log(logging.INFO, "Redirecting to: " + redirect_url)
        print("Redirect url: " + redirect_url)
        return JsonResponse({'url': redirect_url})
        # return redirect(redirect_url)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        # username = kwargs.get('username', 'None')
        # body = json.loads(request.data)
        username = request.GET.get('username')
        return self.get_redirect(username)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        return self.get_redirect(username)


# This endpoint/url is called after a user follows redirect to login into spotify.
class SpotifyCallbackView(LoginView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        username = request.GET.get('state').split('username-')[1]

        user, created = User.objects.get_or_create(username=username)
        status = "Success." if services.authenticate(user, auth_code) else "Failed."

        return JsonResponse({"status": status})