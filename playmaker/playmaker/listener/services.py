import logging


def checkPlaySeek(user):
    actor = user.actor
    if user.is_listener or actor.mode == 'curate':  # Causes current queue song to play for controller as well.
        current_group_song = actor.group.current_song()
        if current_group_song != user.current_song() and user.active_device:
            user.sp.start_playback(user.active_device.sp_id, uris=[actor.group.current_song()])
            user.sp.seek_track(actor.group.current_offset())
        elif not user.active_device:
            logging.log(logging.ERROR, "User: " + user.username + " does not have an active device.")
            return None
    return actor.group.current_song(detail=True)