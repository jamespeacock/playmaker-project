import django
from rest_framework.test import APITestCase, APIClient

from playmaker.controller import services
from playmaker.controller.services import TOP_ARTISTS, ACTIONS
from playmaker.models import User
from playmaker.controllers.models import Permission
from controller.models import Controller, Listener


class PermissionSetupTest(APITestCase):
    client = APIClient()

    def setUp(self):

        # set up Jake Peacock fb spotify account here as tester username
        User.objects.create(username="tester", refresh_token='AQCDZ58fU34wxyDikE-e6nupMc--dq9_8LZf6x0kmB1wi-RuGGvUnZRjCpSY3LeMATuuupQZlqD8akCj8svgNy5qa3BjoCV1fB0cfaPDIdP5L8JHJ8d_G958TtRoUCTh296BsQ')

        # Create Listener & Controller with tester User
        c = Controller.objects.create(me=User.objects.filter(username='tester').first())  # might need to be a fixture at some point
        l = Listener.objects.create(me=User.objects.filter(username='tester').first())

        # Create Permission object
        Permission.objects.create(actor=c, listener=l, scope="ALL")
        self.c_id = c.id
        self.l_id = l.id


class PermissionTest(PermissionSetupTest):

    def test_user_perform_action(self):
        """
        This test ensures that a user object is properly initialized on login.
        All devices, recent artists, top_artists, tokens, etc. are validated after initialization
        """

        listener = Listener.objects.get(id=self.l_id)
        controller = Controller.objects.get(id=self.c_id)
        listener.refresh_listener()

        assert len(listener.devices.all()) > 0
        assert 'Artist ' in listener.top_artists()
        assert 'Artist2 ' in listener.recent_artists()

        results = services.perform_action(controller, [listener], TOP_ARTISTS)

        # Validate Devices, Recent Artists, Top_Artists on listener user
        # TODO Validate custom async action to Mocked Listeners
        assert results is not None

    def test_does_not_have_action_permission(self):
        pass

    def test_bulk_permission_action(self):
        pass

    def test_partial_batch_no_permission(self):
        pass

