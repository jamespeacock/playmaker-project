from django.db import models

# Create your models here.
from django.db.models import DateTimeField, CharField, TextField


class Feedback(models.Model):
    CHOICES = (("Bug/Problem", "Bug/Problem"),
               ("Feature Request", "Feature Request"))
    submitted = DateTimeField(auto_now=True)
    user = CharField(max_length=256)
    type = CharField(max_length=128, choices=CHOICES)
    description = TextField()
