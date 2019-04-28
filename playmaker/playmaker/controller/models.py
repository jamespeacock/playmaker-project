from django.db import models


class Device(models.Model):
    sp_id = models.CharField(max_length=64, null=False)
    is_active = models.BooleanField()
    is_private_session = models.BooleanField()
    is_restricted = models.BooleanField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    volume_percent = models.IntegerField()

