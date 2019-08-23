import asyncio
import logging

from django.core.exceptions import ObjectDoesNotExist
from playmaker.controller.contants import CONTROLLER, LISTENER
from playmaker.controller.models import Listener, Permission, Controller
from playmaker.controller.visitors import Action
from playmaker.models import User
from playmaker.songs.models import Song
from playmaker.songs.serializers import SongSerializer
from playmaker.songs.services import fetch_songs

TOP_ARTISTS = "current_user_top_artists"
ACTIONS = []


def user_matches_actor(user, actor_id, cls):
    # Is it wasteful to pass entire object
    try:
        return cls.objects.get(id=int(actor_id)).me.id == user.id
    except ObjectDoesNotExist:
        return False


def can_perform_action(user, controller, listener_id, action, scope="ALL"):
    return True

    # Check User to controller permission
    assert user_matches_actor(user, controller)


    # Check controller to listener permission
    # permission = Permission.objects.filter(actor=controller, listener=listener_id).first()
    # if permission is not None and scope in permission.scope:
    #     return True
    # else:
    #     logging.log(logging.ERROR, "Controller %i does not have access to listener %i. Action %s" %
    #                 (controller.id, listener_id, action))


# async latee
def kickoff_request(v, action, *args, **kwargs):
    return v.execute(action, *args, **kwargs)


def perform_action(user, controller_uuid, action, *args, **kwargs):

    # Verify ActionPermission object
    controller = Controller.objects.get(id=controller_uuid) # TODO switch to uuid

    # Is this the right place to do can_perfom_action?
    listeners = [listener for listener in controller.listeners if can_perform_action(user, controller, listener, str(action))]

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
    c_id = params.get(CONTROLLER, None)
    l_id = params.get(LISTENER, None)

    # TODO Try to get queue directly from user
    actor_cls, uuid = Controller,c_id if c_id else (Listener,l_id if l_id else None)

    if actor_cls:
        assert user_matches_actor(user, uuid, actor_cls)
        actor = actor_cls.objects.get(uuid=uuid)
        return as_views(actor.get_queue(), SongSerializer)
    else:
        print("User does not have an associated queue.")
        return []


def update_queue_order(uuid, uris):
    pass


def add_to_queue(uuid, uris):
    actor = User.objects.get(uuid=uuid)
    songs = fetch_songs(actor, uris)
    [(s.save(), actor.queue.add(s)) for s in songs]
    # TODO validation here
    return True


def remove_from_queue(uuid, uris):
    actor = User.objects.get(uuid=uuid)
    songs = Song.objects.filter(uri__in=uris).all()
    [actor.queue.remove(s) for s in songs]
    return True