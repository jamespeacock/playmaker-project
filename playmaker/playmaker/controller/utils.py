from playmaker.controller.models import Device

START_PLAYBACK = 'start_playback'


def save_devices(listener, devices):
    listener.devices = [Device(**d) for d in devices]