from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePage(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(path='/')
        self.assertTemplateUsed(response=response, template_name='lists/home.html')

    def test_can_save_post_request(self):
        response = self.client.post(path='/', data={'item_text': 'A new list item'})

        self.assertIn(member='A new list item', container=response.content.decode())
        self.assertTemplateUsed(response=response, template_name='lists/home.html')

