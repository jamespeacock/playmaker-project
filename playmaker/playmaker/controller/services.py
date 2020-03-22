import logging
import threading
import time
from collections import defaultdict

import polling
import requests
from django.core.exceptions import ObjectDoesNotExist

from api.settings import HOSTNAME
from playmaker.controller.contants import URI, URIS
from playmaker.controller.models import SongInQueue, Controller, Queue, Group
from playmaker.controller.visitors import Action
from playmaker.models import User
from playmaker.shared.utils import make_iterable
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


def can_perform_action(actor, listener_uuid, action, scope="ALL"):

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


def perform_action(actor, action, *args, **kwargs):
    # Is this the right place to do can_perform_action?
    listeners = [listener for listener in actor.listeners if can_perform_action(actor, listener, str(action))]

    # Filter out listeners without active devices
    # TODO Just verify all listeners have a selected device. Notify those who dont?
    listeners = [l for l in listeners if l.active_device]

    # Time how long this takes - are either Spotipy and ActionVisitor being instanced?
    visitors = [l.v for l in listeners]
    active_devices = [l.active_device.sp_id for l in listeners]

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


def perform_action_for_listeners(*args, **kwargs):
    kwargs[URIS] = make_iterable(kwargs.pop(URIS))
    failed_results = [r for r in perform_action(*args, **kwargs) if r]

    return len(failed_results) == 0


def as_views(items, serializer):
    return [serializer(instance=item).data for item in items]


## Queue related actions

def get_queue(actor):
    if actor:
        songs = as_views(actor.queue.contents(), QueuedSongSerializer)
        seen = defaultdict(int)
        for s in songs:
            s['position'] = s.pop('in_q')[seen[s[URI]]]
            s['album'] = s.pop('on_album')
            seen[s[URI]] += 1
        return songs
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
    queue.current_song = ns.uri
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
    if songs:
        [SongInQueue.objects.get(song=s, queue=actor.queue, position=positions[i]).delete() for i, s in enumerate(songs)]
        return True
    else:
        return False


"""
Polling for Song changes object
"""


class CurrentSongPoller(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, user, check_current_song, callback, current_song_id=None, *args):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        thread = threading.Thread(target=self.run, args=(user, check_current_song, current_song_id))
        thread.daemon = True                            # Daemonize thread
        self.thread = thread
        self.callback = callback# Start the execution
        self.args = args

    def check_changed(self, response, current_song_id):
        return response['item']['id'] != current_song_id if (response and response['item']) else False

    def start(self):
        self.thread.start()

    def run(self, user, check_current_song, current_song_id):
        logging.log(logging.INFO, "Start polling")

        song_changed = polling.poll(
            lambda: check_current_song(user.sp),
            check_success=lambda response: self.check_changed(response, current_song_id),
            step=2, # Is this every 10s?
            # ignore_exceptions=(requests.exceptions.ConnectionError,),
            poll_forever=True)
        actor = user.actor
        group = actor.group
        if song_changed:
            logging.log(logging.INFO, "Song has changed for group: " + str(group.id))

        # Set current song and push out to all listeners. Do I have access to response
        next_song = song_changed['item']
        current_song_pos = song_changed['progress_ms']

        # Handle curate next song in queue playing
        if actor.mode == 'curate':
            next_song = next_in_queue(group.queue)

        if not next_song:
            next_song = group.play_suggested_song()
        success = perform_action_for_listeners(actor, Action.PLAY, uris=[next_song])
        success = success and perform_action_for_listeners(actor, Action.SEEK, position_ms=current_song_pos)
        group.current_song(refresh=True)

        self.callback(*self.args)  # Kickoff self again with calculated delay.
        return success


def check_song_with_delay(mode, sp_client):
    song = sp_client.currently_playing()
    if song:
        intro_left = 30000 - song['progress_ms']
        remaining = song['item']['duration_ms'] - song['progress_ms']
        if intro_left > 0:
            delay = intro_left
        elif remaining < 3000 and mode == 'curate':
            return None
        else:
            delay = min(120000, round(remaining * 0.8))
        time.sleep(delay)
        song = sp_client.currently_playing()
    return song


def start_polling(user):
    check_current_song = check_song_with_delay
    curr_song = user.sp.currently_playing()
    # TODO check in future if "currently_playing_type" is different from track. If so grab tracks not direct ID
    current_song_id = curr_song['item']['id'] if (curr_song and curr_song['item']) else None

    if current_song_id and user.shouldPoll:
        logging.log(logging.INFO, "Current song before polling: " + str(current_song_id))
        song_poller = CurrentSongPoller(user, check_current_song, start_polling, current_song_id)
        song_poller.start()
        return True
    elif not user.shouldPoll:
        logging.log(logging.INFO, "Polling for song ended.")
    else:
        logging.log(logging.ERROR, "Cannot get controller's current song. Cannot begin polling.")


def stop_polling(user):
    user.shouldPoll = False
    user.save()
    logging.log(logging.INFO, "Stop polling")
    return True


def create_controller_and_group(user, mode):
    controller, created = Controller.objects.get_or_create(me=user)
    if mode:
        controller.mode = mode
    Queue.objects.get_or_create(controller=controller)
    group, created = Group.objects.get_or_create(controller=controller)
    controller.save()
    if not created:
        logging.log(logging.INFO, "Group was not created for some reason! It already existed.")

    return group.id, controller.id