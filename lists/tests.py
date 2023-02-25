from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List


class HomePage(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(path='/')
        self.assertTemplateUsed(response=response, template_name='lists/home.html')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.list = list_
        second_item.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists.count(), 1)

        saved_list = saved_lists[0]
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "The second list item")
        self.assertEqual(second_saved_item.list, list_)


class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post(path='/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post(path='/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, expected_url='/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, template_name='lists/list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, text='Item 1')
        self.assertContains(response, text='Item 2')


