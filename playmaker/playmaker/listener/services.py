

def checkPlaySeek(user):
    actor = user.actor
    if user.is_listener or actor.mode == 'curate':  # Causes current queue song to play for controller as well.
        current_group_song = actor.group.current_song()
        if current_group_song != user.current_song():
            user.sp.start_playback(user.active_device.sp_id, uris=[actor.group.current_song()])
            user.sp.seek_track(actor.group.current_offset())
    return actor.group.current_song(detail=True)