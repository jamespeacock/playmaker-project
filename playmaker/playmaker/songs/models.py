from django.db import models
from django.contrib.auth.models import AbstractUser


class Song(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    #TODO figure out how to store this more secuely
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    scope = models.CharField(max_length=255, null=True, blank=True)
