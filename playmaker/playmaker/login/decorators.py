from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from requests.exceptions import HTTPError
from social_django.utils import load_strategy


def spotify_view(function):
    @login_required
    def wrap(request, *args, **kwargs):
        social = request.user.social_auth.get(provider='spotify')
        token = social.get_access_token(load_strategy())
        try:
            return function(request, token, *args, **kwargs)
        except HTTPError as e:
            print(f'Failed using token because of HTTPError: "{e}"')
            return redirect('logout')
