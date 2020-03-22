import traceback
from enum import Enum

from spotipy import SpotifyException


class Action(Enum):
    PLAY = "play"
    PAUSE = "pause"
    NEXT = "next"
    CURRENT = "now"
    SEEK = "seek"
    NULL = None


class ActionVisitor(object):
    def __init__(self, sp, username, *args, **kwargs):
        self.sp = sp
        self.username = username

        self.action_options = {
            Action.PLAY: sp.start_playback,
            Action.PAUSE: sp.pause_playback,
            Action.NEXT: sp.next_track,
            Action.CURRENT: sp.current_playback,
            Action.SEEK: sp.seek_track,
        }
    """
    
    Visitor execution method for calling 
    
    
    @:param - sp is an intialized and authorized Spotipy instance
    """
    # async later
    def execute(self, action, *args, **kwargs):
        try:
            call = self.action_options[action]
            # This returns a ___ ??
            result = call(*args, **kwargs)
            if call == Action.PLAY:
                pass
                #TODO ensure current_playback matches uri in kwargs
            # end here
        except SpotifyException as e:
            print(traceback.format_exc())
            return {"error": "Error occurred for sp client %s: %s" % (self.username, e)}

    @classmethod
    def get_visitor(cls, *args):
        try:
            return cls(*args)
        except Exception as e:
            print(type(e))
            print(e)
            return Action.NULL