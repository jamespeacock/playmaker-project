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
    token = models.CharField(max_length=255, null=True, blank=True)
