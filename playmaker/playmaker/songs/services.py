
# Fetch and save songs

def nice_images(imgs):
    images = {}
    images['lg'] = imgs[0]
    images['md'] = imgs[1]
    images['sm'] = imgs[2]
    return images


def align_sp_song(sp_song):
    # details = sp_client.audio_features(tracks=[sp_song['item']['uri']])
    song = sp_song['item']
    album = song['album']
    song['albums'] = album
    song['album'] = album['name']
    song['images'] = nice_images(album['images'])
    song['position_ms'] = sp_song['progress_ms']
    return song