
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import unittest

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
    
    def testCheckHomePage(self):

        # I open the Todo app to check out its homepage
        self.browser.get("http://localhost:8000")

        # I check the page title and that it mentions To-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail("Complete the test")



# I get an option to add a new list item after I open the page

# I write 'Watch some interesting anime' into a text box
# 
# After hitting enter, the list gets updated and shows the entered item

# I still get an option to add another item and add other item "Watch Steins;Gate 0 anime"

# The page updates again and the item gets added and shows both items

# The page shows a unique URL for the list which opens the list in the browser

# browser.quit()

if __name__ == '__main__':
    unittest.main()