
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # I open the Todo app to check out its homepage
        self.browser.get(self.live_server_url)

        # I check the page title and that it mentions To-do list
        page_title = self.browser.title
        self.assertEqual(page_title, 'To-Do List')

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # I get an option to add a new list item after opening the page
        input_text = self.browser.find_element(By.ID, 'new_item')
        self.assertEqual(input_text.get_attribute('placeholder'), 'Enter a To-Do item')

        # I write 'Watch some interesting anime' into the text box
        input_text.send_keys("Watch some interesting anime")
        # After hitting enter, the list gets updated and shows the entered item
        input_text.send_keys(Keys.ENTER)
        self.wait_for_row_in_table(row_text="1: Watch some interesting anime")

        # I still get an option to add another item to the list and therefore add 'Watch Steins;Gate 0 ASAP'
        input_text = self.browser.find_element(By.ID, 'new_item')
        self.assertEqual(input_text.get_attribute('placeholder'), 'Enter a To-Do item')
        input_text.send_keys("Watch Steins;Gate 0 ASAP")
        input_text.send_keys(Keys.ENTER)

        # The page updates again and shows both items now
        self.wait_for_row_in_table(row_text="1: Watch some interesting anime")
        self.wait_for_row_in_table(row_text="2: Watch Steins;Gate 0 ASAP")

        # Satisfied, I do my other tasks

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # I create a new to-do list
        self.browser.get(self.live_server_url)
        input_text = self.browser.find_element(By.ID, 'new_item')
        input_text.send_keys("Watch some interesting anime")
        input_text.send_keys(Keys.ENTER)
        self.wait_for_row_in_table(row_text="1: Watch some interesting anime")

        # I notice that my list has a unique URL
        my_list_url = self.browser.current_url
        self.assertRegex(my_list_url, '/lists/.+')

        # Now, my sister also wants to create a new list
        ## We create a new browser session to add her list items and 
        ## make sure that my list is not present for her
        self.browser.quit()
        print("Completed the test for my list. Now moving to my sister's")
        self.browser = webdriver.Chrome(service=Service('static/chromedriver.exe'))

        # My sister visits the homepage and there is no sign of my list
        self.browser.get(self.live_server_url)
        full_page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn("Watch some interesting anime", full_page_text)

        # My sister adds a new item to the list
        # And verifies it is centered as well
        input_text = self.browser.find_element(By.ID, 'new_item')
        input_text.send_keys("Watch vlogs on YouTube")
        input_text.send_keys(Keys.ENTER)
        self.wait_for_row_in_table(row_text="1: Watch vlogs on YouTube")

        # My sister gets her own URL
        sister_list_url = self.browser.current_url
        self.assertRegex(sister_list_url, '/lists/.+')
        self.assertNotEqual(my_list_url, sister_list_url)

        # Again, no trace of my list
        full_page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn("Watch some interesting anime", full_page_text)
