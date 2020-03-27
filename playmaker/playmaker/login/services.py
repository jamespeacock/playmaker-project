import logging
import traceback
from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyOauthError
import six.moves.urllib.parse as urllibparse
from api.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE


def get_redirect(username, frontend_redirect='login'):

    url = 'https://accounts.spotify.com/authorize'
    urlparams = urllibparse.urlencode({'client_id': SPOTIFY_CLIENT_ID, 'response_type': 'code',
                                       'redirect_uri': SPOTIFY_REDIRECT_URI, 'scope': SPOTIFY_SCOPE,
                                       'state': 'username=' + username + '|frontend_redirect=' + frontend_redirect})
    return '%s?%s' % (url, urlparams)


def get_auth(username):
    return SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE,
                        state='username-' + username)


# Responsible for authenticating user via spotify api. Create user object if successful and save is true
def authenticate(user, auth_code, save=True):
    sp_oauth = get_auth(user.username)
    try:
        token_info = sp_oauth.get_access_token(auth_code)
    except SpotifyOauthError:
        logging.log(logging.ERROR, "Authentication exception for %s: \n%s" % (user.username, traceback.format_exc()))
        return False
    # Get or create user based on username, save token info to User object, return success.
    if save:
        user.save_token(token_info)
    return True


#TODO prompt user to authorize login if refresh devices fails or if not linked with spotify at all
def do_refresh_token(user):
    sp_oauth = get_auth(user.username)

    try:
        token_info = sp_oauth.refresh_access_token(user.refresh_token)
        if not token_info:
            logging.log(logging.ERROR, "Refresh token failed for " + user.username)
            return ""
    except ConnectionError:
        return ""

    user.save_token(token_info)
    return user.access_token

