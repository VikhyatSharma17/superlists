from django.test import TestCase

from lists.models import Item, List


class HomePage(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(path='/')
        self.assertTemplateUsed(response=response, template_name='lists/home.html')


class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post(path='/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post(path='/lists/new', data={'item_text': 'A new list item'})
        first_list = List.objects.first()
        self.assertRedirects(response, expected_url=f'/lists/{first_list.id}/')

    def test_can_save_POST_request_to_an_existing_list(self):
        new_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(f'/lists/{new_list.id}/add-item', data={'item_text': 'New item in existing list'})
        self.assertEqual(Item.objects.count(), 1)
        
        created_item = Item.objects.first()
        self.assertEqual(created_item.text, 'New item in existing list')
        self.assertEqual(created_item.list, new_list)

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(f'/lists/{new_list.id}/add-item', data={'item_text': 'New item in an existing list'})
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_passes_correct_list_to_template(self):
        new_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get(f'/lists/{new_list.id}/')
        self.assertEqual(response.context['list'], new_list)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get(f'/lists/{new_list.id}/')
        self.assertTemplateUsed(response, template_name='lists/list.html')

    def test_displays_all_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Other Item 1', list=other_list)
        Item.objects.create(text='Other Item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, text='Item 1')
        self.assertContains(response, text='Item 2')
        self.assertNotContains(response, text='Other Item 1')
        self.assertNotContains(response, text='Other Item 2')


