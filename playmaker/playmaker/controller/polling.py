import logging
import threading

import polling

from playmaker.controller.services import perform_action
from playmaker.controller.visitors import Action


class PollingThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, user, current_song_id=None):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        thread = threading.Thread(target=self.run, args=(user, current_song_id))
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def check_changed(self, response, current_song_id):
        print("Checking if song changed.")
        print(response)
        print(current_song_id)
        return response and response['track']['id'] == current_song_id

    def run(self, user, current_song_id=None, current_song_pos=0):
        #TODO smart polling idea. Wait until halfway between current pos and end of song all the way down to Xs (5 or 10s)
        logging.log(logging.INFO, "Start polling")
        check_current_song = user.sp.currently_playing
        curr_song = check_current_song()
        current_song_id = curr_song['track']['id'] if curr_song else None
        song_changed = polling.poll(
            lambda: check_current_song(),
            check_success=lambda response: self.check_changed(response, current_song_id),
            step=10,
            # ignore_exceptions=(requests.exceptions.ConnectionError,),
            poll_forever=True)

        if song_changed:
            song_changed.close()

        # Set current song and push out to all listeners. Do I have access to response
        next_song = check_current_song()['track']['id']
        if next_song:
            failed_results = [r for r in perform_action(
                user,
                Action.PLAY,
                uris=[next_song.uri]) if r]

        if failed_results:
            logging.log(logging.ERROR, "Failed PLAY results: " + str(failed_results))
        else:
            print("Successfully updated song for listeners.")
            logging.log(logging.INFO, "Successfully updated song for listeners.")
    # Handle failures here
    # Handle kickoff of start polling again -> wait 90s minimum then poll every 10s
