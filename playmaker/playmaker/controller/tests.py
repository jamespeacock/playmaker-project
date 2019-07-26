import pytest

from playmaker.models import User
from playmaker.controller.models import Controller, Listener, Permission


def create_controller():
    try:
        user = User.objects.get(username="test_user")
    except Exception:
        raise Exception("Need to create test_user")

    return Controller.objects.get_or_create(me=user)


def test_visitor_execute():
    pass


@pytest.mark.django_db
def test_can_perform_action_sucess():
    # write this test then implement database
    controller = create_controller()


def test_can_perform_action_fail():
    pass


def test_perform_action():
    pass


# In controller app tests, test you can move songs from controller queue into listener's next up
def test_add_to_controller_queue():
    pass


def test_add_to_listeners_queue():
    pass


def test_add_to_listeners_nextup():
    pass

