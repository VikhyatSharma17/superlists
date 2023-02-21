
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase

import time

# # I open my Todo app to check out its homepage
# browser.get("http://localhost:8000")

# # I check the page title and it mentions To-do lists
# assert "To-Do" in browser.title, f"Browser title was: {browser.title}"

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(service=Service('static/chromedriver.exe'))

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_table(self, row_to_check):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_to_check, [row.text for row in rows])
                return True
            except (WebDriverException, AssertionError) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_check_home_page(self):

        # I open the Todo app to check out its homepage
        self.browser.get(self.live_server_url)

        # I check the page title and that it mentions To-do lists
        self.assertIn('To-Do', self.browser.title)
        headerText = self.browser.find_element(
            By.TAG_NAME,
            'h1'
        ).text
        self.assertIn('To-Do', headerText)

        # I get an option to add a new list item after I open the page
        inputBox = self.browser.find_element(By.ID, 'new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a To-Do item'
        )

        # I write 'Watch some interesting anime' into a text box
        inputBox.send_keys("Watch some interesting anime")

        # After hitting enter, the list gets updated and shows the entered item
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Watch some interesting anime")

        # I still get an option to add another item and add other item "Watch Steins;Gate 0 anime"
        inputBox = self.browser.find_element(By.ID, 'new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a To-Do item'
        )
        inputBox.send_keys("Watch Steins;Gate 0 anime")
        inputBox.send_keys(Keys.ENTER)

        # The page updates again and the item gets added and shows both items
        self.wait_for_row_in_table("1: Watch some interesting anime")
        self.wait_for_row_in_table("2: Watch Steins;Gate 0 anime")

        
        self.fail("Complete the test")


# The page shows a unique URL for the list which opens the list in the browser

# browser.quit()
