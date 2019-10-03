from time import sleep
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response

from api.settings import FRONTEND
from playmaker.login import services
from playmaker.login.services import get_redirect
from playmaker.models import User
from playmaker.shared.views import SecureAPIView


def is_logged_in(request):
    return request.user and hasattr(request.user, 'token') and len(request.user.token)


class SpotifyRegisterView(RegisterView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.data
        username = body.get('username')
        frontend_redirect = body.get('redirect', 'login')
        signup = super(SpotifyRegisterView, self).post(request, *args, **kwargs)
        if signup.status_code != 201:
            return JsonResponse(signup, safe=False, status=400)
        return JsonResponse({'url': get_redirect(username, frontend_redirect=frontend_redirect)})


class SpotifyLoginView(LoginView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # TODO check if request already has user and is logged in.
        data = request.data
        frontend_redirect = data.get('redirect', 'login')
        if is_logged_in(request):
            # User is already logged in --> send to dashboard.
            return redirect(FRONTEND + "/" + frontend_redirect)

        login = super(SpotifyLoginView, self).post(request, *args, **kwargs)
        assert login.status_code == 200
        username = data.get('username')
        return JsonResponse({'url': get_redirect(username, frontend_redirect=frontend_redirect)})


# This endpoint/url is called after a user follows redirect to login into spotify.
class SpotifyCallbackView(LoginView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        args = request.GET.get('state').split('|')
        username = args[0].split('username=')[1]
        redirect_path = args[1].split('frontend_redirect=')[1]
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print('User does not exist for some reason.')
        return redirect(FRONTEND + "/" + redirect_path) if services.authenticate(user, auth_code) else JsonResponse({"status": "Login Failed."})


class IsLoggedInView(SecureAPIView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        super(IsLoggedInView, self).get(request)
        return Response({'user': {
            'username': request.user.username,
            'sp_username': request.user.sp_username,
            'sp_id': request.user.sp_id,
            'isLoggedIn': True}
        })


class LogoutView(LogoutView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        super(LogoutView, self).post(request, *args, **kwargs)
        # Not used, but example for how to fix CORS null Origin on redirect
        response = redirect(FRONTEND + "/login")
        response['Origin'] = FRONTEND
        return response
