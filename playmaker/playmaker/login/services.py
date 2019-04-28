import spotipy
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from playmaker.models import User


def authenticate(username, auth_code):
    sp_oauth = spotipy.oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                                           SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE, state='username-' + username)
    token_info = sp_oauth.get_access_token(auth_code)

    # Get user based on username, save token info to User object, return success.
    user, created = User.objects.get_or_create(username=username)

    return user.save_token(token_info)