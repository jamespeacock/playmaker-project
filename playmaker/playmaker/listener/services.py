

def checkPlaySeek(actor, is_listener):
    if is_listener:
        current_group_song = actor.group.current_song()
        if current_group_song != actor.current_song():
            actor.me.sp.start_playback(actor.active_device.sp_id, uris=[actor.group.current_song()])
            actor.me.sp.seek_track(actor.group.current_offset())
    return actor.group.current_song(detail=True)