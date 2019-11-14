from django.db import models

# Create your models here.
from django.db.models import DateTimeField, CharField, TextField


class Feedback(models.Model):
    submitted = DateTimeField()
    user = CharField(max_length=256)
    type = CharField(max_length=128, choices=("Bug/Problem", "Feature Request"))
    description = TextField()
