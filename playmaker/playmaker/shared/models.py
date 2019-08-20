from django.db import models


class SPModel(models.Model):
    sp_id = models.CharField(max_length=255, unique=True)
    href = models.CharField(max_length=511)