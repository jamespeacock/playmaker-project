from django.core.management.base import BaseCommand, CommandError

from playmaker.controller.models import Listener, Group
from playmaker.controller.services import create_controller_and_group, perform_action
from playmaker.controller.visitors import Action
from playmaker.models import User

USERNAME = "test_controller"
SONG_URIS = [
    'spotify:track:4FjT3dqUW2Uq0R3pMz5V7C',  # Help Me Lose My Mind
    'spotify:track:7uaixPPB670BtzMKTu4Ljp',  # Energy
    'spotify:track:7pD6katrwWH7H3Xt8cIZS9'  # Lemonglow
]

class Command(BaseCommand):
    help = 'Initializes a controller and a room for dev testing.'

    def add_arguments(self, parser):
        parser.add_argument('--users', help='Auto add users to the group created.')

    def handle(self, *args, **options):
        u, _ = User.objects.get_or_create(username=USERNAME)
        g_id, c_id = create_controller_and_group(u)
        print("Created group number: " + str(g_id))

        users = options['users'] or []
        for user in users:
            l, _ = Listener.objects.get_or_create(me=user, group=Group.objects.get(id=g_id))

        for song_uri in SONG_URIS:
            input("Press Enter to play next song!")
            failed_results = [r for r in perform_action(
                u,
                Action.PLAY,
                uris=[song_uri]) if r]
            if failed_results:
                print("Failed to play for all users in group!")
                print(failed_results)
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))