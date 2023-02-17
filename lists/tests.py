from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePage(TestCase):

    def test_root_url_resolves_to_home_page(self):
        rootURL = resolve('/')

        self.assertEqual(rootURL.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        
        htmlCode = response.content.decode('utf-8')
        print(htmlCode)


        self.assertTrue(htmlCode.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', htmlCode)
        self.assertTrue(htmlCode.endswith('</html>'))

