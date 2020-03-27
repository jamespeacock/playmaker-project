import logging
import traceback

from api.settings import DEFAULT_MS_OFFSET


def checkPlaySeek(user):
    try:
        actor = user.actor
        if user.is_listener or actor.mode == 'curate':  # Causes current queue song to play for controller as well.
            current_room_song = actor.room.current_song(detail=False)
            if current_room_song != user.current_song() and current_room_song and user.active_device:
                user.sp.start_playback(user.active_device.sp_id, uris=[current_room_song])
                offset = actor.room.current_offset()
                if offset > DEFAULT_MS_OFFSET:
                    user.sp.seek_track(offset)
            elif not user.active_device:
                logging.log(logging.ERROR, "User: " + user.username + " does not have an active device.")
                return None
            elif not current_room_song:
                logging.log(logging.ERROR, "There is no longer a room song.")
                return None
        return actor.room.current_song(detail=True)
    except AttributeError:
        logging.log(logging.ERROR, user.username + "'s room no longer exists.")
        logging.log(logging.DEBUG, traceback.format_exc())
        return None