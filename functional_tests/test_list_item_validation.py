
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_blank_list_item(self):
        # I go the homepage and accidentally add blank list item 
        # by pressing enter on the empty list item field.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'new_item').send_keys(Keys.ENTER)


        # The home page refreshes and shows an error message that the list item cannot be blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
                "You can't have an empty list item!"
            )
        )

        # I try again with some text in the list item and it works
        self.browser.find_element(By.ID, 'new_item').send_keys("Do stuff")
        self.browser.find_element(By.ID, 'new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Do stuff")

        # I again try to add empty list item and gets the same error
        self.browser.find_element(By.ID, 'new_item').send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, '.has-error').text, 
                "You can't have an empty list item!"
            )
        )

        # I then add the correct list item
        self.browser.find_element(By.ID, 'new_item').send_keys("Do more stuff")
        self.browser.find_element(By.ID, 'new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Do stuff")
        self.wait_for_row_in_table("2: Do more stuff")