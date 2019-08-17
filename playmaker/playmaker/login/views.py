import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView

from api.settings import FRONTEND
from playmaker.login import services
from playmaker.login.services import get_redirect
from playmaker.models import User


class SpotifyRegisterView(RegisterView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        what = super(SpotifyLoginView, self).post(request, *args, **kwargs)
        body = json.loads(request.body)
        username = body.get('username')
        # TODO do initial user creation via django user auth with user/pwd first--> then do redirect

        return JsonResponse({'url': get_redirect(username)})


class SpotifyLoginView(LoginView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # TODO check if request already has user and is logged in.
        body = json.loads(request.body)
        login = super(SpotifyLoginView, self).post(request, *args, **kwargs)
        assert login.status_code == 200
        username = body.get('username')
        return JsonResponse({'url': get_redirect(username)})


# This endpoint/url is called after a user follows redirect to login into spotify.
class SpotifyCallbackView(LoginView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        username = request.GET.get('state').split('username-')[1]

        user, created = User.objects.get_or_create(username=username)
        # TODO is /dashboard permanent or can this go into state?? ^^
        return redirect(FRONTEND + "/dashboard") if services.authenticate(user, auth_code) else JsonResponse({"status": "Login Failed."})
