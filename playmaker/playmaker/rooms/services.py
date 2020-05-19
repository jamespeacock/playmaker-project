
# Queue related actions
from collections import defaultdict

from playmaker.controller.contants import URI
from playmaker.models import User
from playmaker.rooms.models import SongInQueue
from playmaker.shared.models import SPModel
from playmaker.shared.utils import as_views
from playmaker.songs.models import Song
from playmaker.songs.serializers import QueuedSongSerializer, SongSerializer


def get_queue(actor):
    if actor and actor.queue:
        songs = as_views(actor.queue.contents(), QueuedSongSerializer)
        seen = defaultdict(int)
        for s in songs:
            s['position'] = s.pop('in_q')[seen[s[URI]]]
            s['album'] = s.pop('on_album')
            seen[s[URI]] += 1
        return songs
    else:
        print("User does not have both actor & queue currently.")
        return []


def update_queue_order(queue, uris):
    for i, uri in enumerate(uris):
        queue.songs.get(uri=uri).in_q.position = i
    queue.songs.all().save()
    queue.save()


def next_in_queue(queue):
    ns = queue.songs.order_by('in_q').first()
    if not ns:
        print("Queue did not have a next song.")
        queue.current_song = None
        queue.save()
        return None
    queue.current_song = ns.uri
    SongInQueue.objects.get(song=ns, queue=queue).delete()
    queue.save()
    return queue.current_song


def add_to_queue(uuid, uris):
    actor = User.objects.get(uuid=uuid).actor
    if uris:
        sp = actor.me.sp
        songs = SPModel.from_response(sp.tracks(uris), Song, serializer=SongSerializer, save=True)
        next_pos = actor.queue.next_pos
        for s in songs:
            SongInQueue.objects.create(song=s, queue=actor.queue, position=actor.queue.next_pos)
            next_pos += 1
        actor.queue.next_pos = next_pos
        actor.queue.save()
        return True
    else:
        return False


def remove_from_queue(uuid, uris, positions):
    actor = User.objects.get(uuid=uuid).actor
    songs = Song.objects.filter(uri__in=uris).all()
    if songs:
        [SongInQueue.objects.get(song=s, queue=actor.queue, position=positions[i]).delete() for i, s in enumerate(songs)]
        return True
    else:
        return False