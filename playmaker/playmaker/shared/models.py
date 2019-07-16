from django.db import models


class SPModel(models.Model):
    sp_id = models.CharField(max_length=255)
    href = models.CharField(max_length=511)