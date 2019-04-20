from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    #TODO figure out how to store this more secuely - encryptedField
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    scope = models.CharField(max_length=255, null=True, blank=True)