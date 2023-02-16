
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromeService = Service("static/chromedriver.exe")
browser = webdriver.Chrome(service=chromeService)
browser.get("http://localhost:8000")

assert "Congratulations" in browser.title