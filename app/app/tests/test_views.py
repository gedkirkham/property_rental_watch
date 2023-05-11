# from django.test import TestCase
from unittest import TestCase
from django.test import Client
from app.views import HomeView


class HomeViewTestCase(TestCase):
    def setup(self):
        c = Client()
        self.response = c.get("/")

    def test_unauthorised_user_success(self):
        "Test that unauthorised users can access the home page."
        self.assertEqual(200, self.response.status_code)
