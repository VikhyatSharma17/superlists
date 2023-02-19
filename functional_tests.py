
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import unittest
import time

# chromeService = Service("static/chromedriver.exe")
# browser = webdriver.Chrome(service=chromeService)


# # I open my Todo app to check out its homepage
# browser.get("http://localhost:8000")

# # I check the page title and it mentions To-do lists
# assert "To-Do" in browser.title, f"Browser title was: {browser.title}"

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(service=Service('static/chromedriver.exe'))

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_to_check):
        table = self.browser.find_element(By.ID, 'list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_to_check, [row.text for row in rows])

    
    def test_check_home_page(self):

        # I open the Todo app to check out its homepage
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)
        self.check_for_row_in_table("1: Watch some interesting anime")

        # I still get an option to add another item and add other item "Watch Steins;Gate 0 anime"
        inputBox = self.browser.find_element(By.ID, 'new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a To-Do item'
        )
        inputBox.send_keys("Watch Steins;Gate 0 anime")
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and the item gets added and shows both items
        self.check_for_row_in_table("1: Watch some interesting anime")
        self.check_for_row_in_table("2: Watch Steins;Gate 0 anime")

        
        self.fail("Complete the test")


# The page shows a unique URL for the list which opens the list in the browser

# browser.quit()

if __name__ == '__main__':
    unittest.main()