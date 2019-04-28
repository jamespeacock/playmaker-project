import asyncio
import logging

from playmaker.models import Permission

TOP_ARTISTS = "current_user_top_artists"
ACTIONS = []


def can_perform_action(controller, listener, action, scope="ALL"):
    permission = Permission.objects.filter(actor=controller, listener=listener).first()
    if permission is not None and scope in permission.scope:
        return True
    else:
        logging.log(logging.ERROR, "Controller %i does not have access to listener %i. Action %s" %
                    (controller.id, listener.id, action))


async def kickoff_request(action, *args, **kwargs):
    return await action(*args)


# TODO figure out a shared method that executes an action for a bunch of users. ex: all users need a song queued
def perform_action(controller, listeners, action, *args, **kwargs):

    # do asynchronously so that timing can be optimized

    # VERIFY ACTION PERMISSION object
    listeners = [listener for listener in listeners if can_perform_action(controller, listener, str(action))]

    logging.log(logging.INFO, "Performing %s for %i listeners..." % (str(action), len(listeners)))

    loop = asyncio.get_event_loop()
    async_actions = [kickoff_request(action, controller, l, *args, **kwargs) for l in listeners]
    results = loop.run_until_complete(asyncio.gather(*async_actions))

    print(results)

    return results


