from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

class HomePage(TestCase):

    def test_root_url_resolves_to_home_page(self):
        rootURL = resolve('/')

        self.assertEqual(rootURL.func, home_page)