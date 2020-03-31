
# Fetch and save songs


def nice_images(imgs):
    return {'lg': imgs[0], 'md': imgs[1], 'sm': imgs[2]}


def align_sp_song(sp_song):
    # details = sp_client.audio_features(tracks=[sp_song['item']['uri']])
    song = sp_song['item']
    album = song['album']
    song['albums'] = album
    song['album'] = album['name']
    song['images'] = nice_images(album['images'])
    song['position_ms'] = sp_song['progress_ms']
    return song