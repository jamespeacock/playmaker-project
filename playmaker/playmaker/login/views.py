import cProfile
import pstats
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework.exceptions import ValidationError
from django.utils import timezone as tz

from api.settings import FRONTEND
from playmaker.controller.models import Controller
from playmaker.listener.models import Listener
from playmaker.controller.serializers import ControllerSerializer, ListenerSerializer
from playmaker.login import services
from playmaker.login.services import get_redirect
from playmaker.models import User
from playmaker.serializers import UserSerializer
from playmaker.shared.views import SecureAPIView


def is_logged_in(user):
    return user and hasattr(user, 'token') and len(user.token)


class SpotifyRegisterView(RegisterView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.data
        username = body.get('username')
        frontend_redirect = body.get('redirect', 'login')
        try:
            signup = super(SpotifyRegisterView, self).post(request, *args, **kwargs)
            if signup.status_code != 201:
                return JsonResponse(signup, safe=False, status=signup.status_code)
            return JsonResponse({'url': get_redirect(username, frontend_redirect=frontend_redirect)})
        except Exception as e:
            return JsonResponse({"error": self.format_exc(e)}, status=403)

    def format_exc(self, e):
        exc_str = ""
        if isinstance(e, ValidationError):
            for field, detail in e.detail.items():
                exc_str += "%s: " % field
                exc_str += "\n".join([str(err) for err in detail])
                exc_str += "\n"
        else:
            exc_str += str(e)
        return exc_str


class SpotifyLoginView(LoginView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # TODO check if request already has user and is logged in.
        data = request.data
        frontend_redirect = data.get('redirect', 'login')
        if is_logged_in(request.user):
            # User is already logged in --> send to dashboard.
            user = request.usera
            user.last_active = tz.now()
            user.save()
            user_redirect = redirect(FRONTEND + "/" + frontend_redirect)
            return user_redirect
        try:
            login = super(SpotifyLoginView, self).post(request, *args, **kwargs)
        except Exception as e:
            #Todo return more specific exception
            return JsonResponse({"error": "Invalid credentials."}, status=401)
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
        user_redirect = redirect(FRONTEND + "/" + redirect_path)
        return user_redirect if services.authenticate(user, auth_code) else JsonResponse({"status": "Login Failed."})


class IsLoggedInView(SecureAPIView):

    def get_serializer_class(self):
        return UserSerializer

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        # pr = cProfile.Profile()
        # pr.enable()
        super(IsLoggedInView, self).get(request)
        actor = {}
        user = request.user
        u_actor = user.actor
        try:
            ser = None
            if type(u_actor) == Listener:
                ser = ListenerSerializer
            elif type(u_actor) == Controller:
                ser = ControllerSerializer
            if ser:
                actor = ser(u_actor).data
        except (Listener.DoesNotExist, Controller.DoesNotExist):
            pass

        ser = self.get_serializer_class()

        user_data = {**ser(user).data,
         'actor': actor,
         'is_logged_in': is_logged_in(user)}

        if user.token:
            user_data['is_authenticated'] = True
        else:
            user_data['is_authenticated'] = False
        redirect_path = request.GET.get('redirect', 'dashboard')
        redirect_path = 'dashboard' if not redirect_path or redirect_path == 'undefined' else redirect_path
        user_data['auth_url'] = get_redirect(user.username, frontend_redirect=redirect_path)

        # pr.disable()
        # ps = pstats.Stats(pr).sort_stats('tottime')
        # ps.print_stats(20)
        return JsonResponse({'user': user_data})


class LogoutView(LogoutView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            request.user.listener.delete()
            request.user.is_listener = False
            # self.devices.all().delete()
        except Listener.DoesNotExist:
            pass
        try:
            request.user.controller.delete()
            request.user.is_controller = False
            # self.devices.all().delete()
        except Controller.DoesNotExist:
            pass
        request.user.save()
        super(LogoutView, self).post(request, *args, **kwargs)

        return JsonResponse({"success": True})
