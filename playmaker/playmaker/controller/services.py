import logging
import threading
import time

import polling
from django.core.exceptions import ObjectDoesNotExist

from api.settings import DEFAULT_MS_OFFSET, TURN_OFF_IDLE_CONTROLLERS
from playmaker.controller.contants import URIS
from playmaker.controller.models import Controller
from playmaker.rooms.models import Room, Queue
from playmaker.controller.visitors import Action
from playmaker.models import User
from playmaker.rooms.services import next_in_queue
from playmaker.shared.utils import make_iterable

TOP_ARTISTS = "current_user_top_artists"
ACTIONS = []

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')


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


# TODO make async
def kickoff_request(v, action, *args, **kwargs):
    return v.execute(action, *args, **kwargs)


def perform_action(actor, action, *args, **kwargs):
    # Is this the right place to do can_perform_action?
    listeners = [listener for listener in kwargs.pop('listeners', []) or actor.listeners if can_perform_action(actor, listener, str(action))]

    # Filter out listeners without active devices
    # Time how long this takes - are either Spotipy and ActionVisitor being instanced?
    listeners = [(l.v, l.me.active_device.sp_id) for l in listeners if l.me.active_device]

    # Kickoff loops with visitors,devices + action
    # loop = asyncio.get_event_loop()
    logging.info("Performing %s for %i listeners..." % (str(action), len(listeners)))
    if action == Action.SEEK:
        results = [kickoff_request(v, action, *args, **kwargs) for v, ad_id in listeners]
    else:
        results = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in listeners]
    # async_actions = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    # results = loop.run_until_complete(asyncio.gather(*async_actions))

    return results # loop.run_until_complete(asyncio.gather(*async_actions))

# TODO FIX polling updating when it shouldn't - CHECK CHAnGED is broken
def check_playing_for_all_listeners(listeners, **kwargs):
    different = [r for r in perform_action(Action.CURRENT, **kwargs) if not r.get('error', None)]
    listeners = [d for d in different if d and d['item'] and d['item']['uri'] != kwargs[URIS][0]]


def perform_action_for_listeners(*args, **kwargs):
    if URIS in kwargs:
        kwargs[URIS] = make_iterable(kwargs.pop(URIS))

    failed_results = [r for r in perform_action(*args, **kwargs) if not r or r.get('error', None)]

    return len(failed_results) == 0


"""
Polling for Song changes object
"""

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def check_song_with_delay(mode, user, thread):
    song = user.sp.currently_playing()
    if song and song['item']:
        intro_left = 30000 - song['progress_ms']

        if intro_left > 0:
            delay = intro_left
        # elif remaining < 3000 and mode == 'curate': # Turn this on to try and end songs a few seconds early
        #     return None
        else:
            remaining = song['item']['duration_ms'] - song['progress_ms']
            delay = min(120000, round(remaining * 0.8))

        if song['progress_ms'] > 10: # Most likely means song is not playing if progress_ms < 10.
            delay = round(delay/1000.0)
            print("About to wait for " + str(delay))
            st = time.time()
            while time.time() - st < delay:
                if thread.stopped():
                    print("Got signal to stop. Exiting.")
                    raise StoppedException()
                time.sleep(1)
        song = user.sp.currently_playing()
    return song


class StoppedException(BaseException):
    pass


class CurrentSongPoller(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, user, callback, current_song_id=None, *args):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        thread = StoppableThread(target=self.run, args=(user, current_song_id))
        thread.daemon = True                            # Daemonize thread
        self.thread = thread
        self.callback = callback# Start the execution
        self.args = args

    def check_changed(self, response, current_song_id):
        if response and response['item'] and response['is_playing']:
            changed = response['item']['id'] != current_song_id
        elif response:
            changed = not response['is_playing']
        else:
            changed = response is None and current_song_id is not None
        return changed

    def start(self):
        self.thread.start()

    def run(self, user, current_song_id):
        if user.hasActivePoller:
            return False
        user.hasActivePoller = True
        user.pollingThread = str(self.thread.ident)
        user.save()
        try: 
            song_changed = polling.poll(
                # Won't work if user is a listener!
                lambda: check_song_with_delay(user.actor.mode, user, self.thread),
                check_success=lambda response: self.check_changed(response, current_song_id),
                step=2,
                poll_forever=True)
        except StoppedException:
            song_changed = user.sp.currently_playing()
            if not self.check_changed(song_changed, current_song_id):
                user.hasActivePoller = False
                user.save()
            return
        actor = user.actor
        room = actor.room
        if song_changed:
            logging.log(logging.INFO, "Song has changed for group: " + str(room.id))

        # Set current song and push out to all listeners. Do I have access to response
        next_song = song_changed['item']['uri'] if song_changed and song_changed['item'] else None
        current_song_pos = song_changed['progress_ms'] if song_changed else 0

        # Handle curate next song in queue playing (overwrite if anything else was playing next for controller)
        if actor.mode == 'curate':
            print("Actor in curate. Going to next song in queue.")
            next_song = next_in_queue(room.queue)
            current_song_pos = 0

        # In all cases, if there is no next song, make sure there is one
        if not next_song:
            print("Playing next suggested song bc no songs were in queue or currently playing.")
            next_song = room.play_suggested_song()
            current_song_pos = 0

        if actor.mode == 'curate':
            # In curate mode, the next song from the queue needs to be played for the controller as well.
            print("Playing next song for controller.")
            user.play_song(next_song)

        success = perform_action_for_listeners(actor, Action.PLAY, uris=[next_song])
        if current_song_pos > DEFAULT_MS_OFFSET:
            success = success and perform_action_for_listeners(actor, Action.SEEK, position_ms=current_song_pos)

        user.hasActivePoller = False
        user.save()
        if user.active:
            logging.info("Restarting polling.")
            self.callback(*(user, *self.args))  # Kickoff self again with calculated delay.
        elif TURN_OFF_IDLE_CONTROLLERS:
            logging.info("Controller is no longer active. Removing")
            user.is_controller = False
            user.controller.delete()
            user.save()
        return success


def start_polling(user):
    curr_song = user.sp.currently_playing()
    # TODO check in future if "currently_playing_type" is different from track. If so grab tracks not direct ID
    current_song_id = curr_song['item']['id'] if (curr_song and curr_song['item'] and curr_song['is_playing']) else None
    logging.log(logging.INFO, "Current song before polling: " + str(current_song_id))
    song_poller = CurrentSongPoller(user, start_polling, current_song_id)
    song_poller.start()
    if not user.hasActivePoller:
        print("New thread did not start.")
        return False

    return True


def find_thread_match(threadId):
    for t in threading.enumerate():
        if str(t.ident) == threadId:
            # Meants t is a stoppable thread.
            return t
    return None


def stop_polling(user):
    t = find_thread_match(user.pollingThread)
    if t and isinstance(t, StoppableThread):
        t.stop()
        print('joining %s', t.getName())
        t.join()
    user.pollingThread = None
    user.hasActivePoller = False
    user.save()
    logging.log(logging.INFO, "Stop polling")
    return True


def create_controller_and_room(user, mode):
    controller, created = Controller.objects.get_or_create(me=user)
    if mode:
        controller.mode = mode
    user.save()
    queue, created = Queue.objects.get_or_create(controller=controller)
    room, created = Room.objects.get_or_create(controller=controller, queue=queue)
    controller.save()
    if not created:
        logging.log(logging.INFO, "Room was not created for some reason! It already existed.")

    if not find_thread_match(user.pollingThread):
        user.pollingThread = None
        user.hasActivePoller = False
        user.save()
        start_polling(user)

    return room, controller.id