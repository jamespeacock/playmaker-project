import asyncio
import logging

from playmaker.controller.models import Listener, Permission, Controller

TOP_ARTISTS = "current_user_top_artists"
ACTIONS = []


def can_perform_action(controller, listener_id, action, scope="ALL"):
    return True
    permission = Permission.objects.filter(actor=controller, listener=listener_id).first()
    if permission is not None and scope in permission.scope:
        return True
    else:
        logging.log(logging.ERROR, "Controller %i does not have access to listener %i. Action %s" %
                    (controller.id, listener_id, action))


# async latee
def kickoff_request(v, action, *args, **kwargs):
    return v.execute(action, *args, **kwargs)


def perform_action(controller_uuid, action, *args, **kwargs):

    # Verify ActionPermission object
    controller = Controller.objects.get(id=controller_uuid) # TODO switch to uuid

    # Is this the right place to do can_perfom_action?
    listeners = [listener for listener in controller.listeners if can_perform_action(controller, listener, str(action))]

    # Filter out listeners without active devices
    listeners = [l for l in listeners if l.refresh()]

    # Time how long this takes - are either Spotipy and ActionVisitor being instanced?
    visitors = [l.v for l in listeners]
    active_devices = [l.devices.filter(is_active=True).first().sp_id for l in listeners]

    # Kickoff loops with visitors,devices + action
    # loop = asyncio.get_event_loop()
    logging.log(logging.INFO, "Performing %s for %i listeners..." % (str(action), len(visitors)))
    results = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    # async_actions = [kickoff_request(v, action, ad_id, *args, **kwargs) for v, ad_id in zip(visitors, active_devices)]
    # results = loop.run_until_complete(asyncio.gather(*async_actions))

    print(results)

    return results # loop.run_until_complete(asyncio.gather(*async_actions))