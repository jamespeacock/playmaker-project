import logging
import threading
from collections import defaultdict

import polling
import requests
from django.core.exceptions import ObjectDoesNotExist

from api.settings import HOSTNAME
from playmaker.controller.contants import URI
from playmaker.controller.models import SongInQueue, Controller, Queue, Group
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
    if songs:
        [SongInQueue.objects.get(song=s, queue=actor.queue, position=positions[i]).delete() for i, s in enumerate(songs)]
        return True
    else:
        return False


"""
Polling for Song changes object
"""


class PollingThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, user, check_current_song, callback, current_song_id=None, current_pos=0, *args):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        thread = threading.Thread(target=self.run, args=(user, check_current_song, current_song_id, current_pos))
        thread.daemon = True                            # Daemonize thread
        self.thread = thread
        self.callback = callback# Start the execution
        self.args = args

    def check_changed(self, response, current_song_id):
        print("Checking if song changed.")
        return response['item']['id'] != current_song_id if (response and response['item']) else False

    def start(self):
        self.thread.start()

    def run(self, user, check_current_song, current_song_id, current_song_pos):
        #TODO smart polling idea. Wait until halfway between current pos and end of song all the way down to Xs (5 or 10s)
        logging.log(logging.INFO, "Start polling")

        song_changed = polling.poll(
            lambda: check_current_song(),
            check_success=lambda response: self.check_changed(response, current_song_id),
            step=10,
            # ignore_exceptions=(requests.exceptions.ConnectionError,),
            poll_forever=True)

        if song_changed:
            logging.log(logging.INFO, "Song has changed.")

        # Set current song and push out to all listeners. Do I have access to response
        next_song = song_changed['item']
        if next_song:
            failed_results = [r for r in perform_action(
                user,
                Action.PLAY,
                uris=[next_song['uri']]) if r]

        if failed_results:
            logging.log(logging.ERROR, "Failed PLAY results: " + str(failed_results))
        else:
            logging.log(logging.INFO, "Successfully updated song for listeners.")

        self.callback(*self.args)
        return True
    # Handle failures here
    # Handle kickoff of start polling again -> wait 90s minimum then poll every 10s


def start_polling(user):
    check_current_song = user.sp.currently_playing
    curr_song = check_current_song()
    # TODO check in future if "currently_playing_type" is different from track. If so grab tracks not direct ID
    current_song_id = curr_song['item']['id'] if (curr_song and curr_song['item']) else None
    current_pos = curr_song['progress_ms'] if curr_song else 0
    # total_duration = curr_song['item']['duration_ms']
    if current_song_id:
        logging.log(logging.INFO, "Current song before polling: " + str(current_song_id))
        song_poller = PollingThread(user, check_current_song, start_polling, current_song_id, current_pos, user)
        song_poller.start()
        return True
    else:
        logging.log(logging.ERROR, "Cannot get controller's current song. Cannot begin polling.")
        return False


def stop_polling(user):
    logging.log(logging.INFO, "Stop polling")
    pass


def create_controller_and_group(user):
    controller, created = Controller.objects.get_or_create(me=user)
    Queue.objects.get_or_create(controller=controller)
    group, created = Group.objects.get_or_create(controller=controller)
    print("group created: " + str(created))
    if not created:
        logging.log(logging.INFO, "Group was not created for some reason! It already existed.")

    return group.id, controller.id