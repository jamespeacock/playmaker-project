import logging

from django.core.exceptions import ObjectDoesNotExist

from playmaker.controller.models import SongInQueue
from playmaker.controller.visitors import Action
from playmaker.models import User
from playmaker.songs.models import Song
from playmaker.songs.serializers import QueuedSongSerializer
from playmaker.songs.services import fetch_songs

TOP_ARTISTS = "current_user_top_artists"
ACTIONS = []


# TODO change this method to ensure user actor matches Listener vs. Controller so that listeners can only do listener actions, etc.
def user_matches_actor(user, actor_uuid, cls):
    # Is it wasteful to pass entire object
    try:
        return cls.objects.get(id=actor_uuid).me.id == user.id and User.objects.get(uuid=user.uuid).auth_token == user.auth_token
    except ObjectDoesNotExist:
        return False


def can_perform_action(user, listener_uuid, action, scope="ALL"):

    # Check User to controller permission
    return True

    # Check controller to listener permission
    # permission = Permission.objects.filter(actor=user.actor, listener=listener_id).first()
    # if permission is not None and scope in permission.scope:
    #     return True
    # else:
    #     logging.log(logging.ERROR, "Controller %i does not have access to listener %i. Action %s" %
    #                 (actor.uuid, listener_id, action))


# TODO async later
def kickoff_request(v, action, *args, **kwargs):
    return v.execute(action, *args, **kwargs)


def perform_action(user, action, *args, **kwargs):
    # Is this the right place to do can_perform_action?
    listeners = [listener for listener in user.actor.listeners if can_perform_action(user, listener, str(action))]

    # Filter out listeners without active devices
    listeners = [l for l in listeners if l.refresh()]

    # Time how long this takes - are either Spotipy and ActionVisitor being instanced?
    visitors = [l.v for l in listeners]
    active_devices = [l.active_device.sp_id for l in listeners if l.active_device]

    # Kickoff loops with visitors,devices + action
    # loop = asyncio.get_event_loop()
    logging.log(logging.INFO, "Performing %s for %i listeners..." % (str(action), len(visitors)))
    if action == Action.SEEK:
        results = [kickoff_request(v, action, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    else:
        results = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    # async_actions = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    # results = loop.run_until_complete(asyncio.gather(*async_actions))

    print(results)

    return results # loop.run_until_complete(asyncio.gather(*async_actions))


def as_views(items, serializer):
    return [serializer(instance=item).data for item in items]


## Queue related actions

def get_queue(params, user):

    if user.actor:
        return as_views(user.actor.queue.contents(), QueuedSongSerializer)
    else:
        print("User does not have an associated listener or controller.")
        return []


def update_queue_order(queue, uris):
    for i, uri in enumerate(uris):
        queue.songs.get(uri=uri).in_q.position = i
    queue.songs.all().save()
    queue.save()


def next_in_queue(queue):
    ns = queue.songs.first()
    if not ns:
        return None
    queue.current_song = ns
    SongInQueue.objects.get(song=ns, queue=queue).delete()
    queue.save()
    return queue.current_song


def add_to_queue(uuid, uris):
    actor = User.objects.get(uuid=uuid).actor
    songs = fetch_songs(actor, uris, save=True)
    songs = Song.objects.filter(uri__in=[s['uri'] for s in songs]).all()
    next_pos = actor.queue.next_pos
    for s in songs:
        SongInQueue.objects.create(song=s, queue=actor.queue, position=actor.queue.next_pos)
        next_pos += 1
    actor.queue.next_pos = next_pos
    actor.queue.save()

    # TODO validation here
    return True


def remove_from_queue(uuid, uris, positions):
    actor = User.objects.get(uuid=uuid).actor
    songs = Song.objects.filter(uri__in=uris).all()
    [SongInQueue.objects.get(song=s, queue=actor.queue, position=positions[i]).delete() for i, s in enumerate(songs)]
    return True