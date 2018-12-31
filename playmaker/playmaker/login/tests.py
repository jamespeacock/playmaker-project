from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()


class SpotifyAuthTest(BaseViewTest):

    def test_spotify_auth(self):
        print("Starting")
        response = self.client.get(reverse("spotify-login"))
        print(response)
        print("Done")