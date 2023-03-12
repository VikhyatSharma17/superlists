
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # I go to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # I notice the input box is nicely centered
        input_box = self.browser.find_element(By.ID, 'new_item')
        input_box.send_keys('Test list item')
        input_box.send_keys(Keys.ENTER)
        input_box = self.browser.find_element(By.ID, 'new_item')
        self.wait_for_row_in_table(row_text='1: Test list item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']//2,
            512,
            delta=10
        )
