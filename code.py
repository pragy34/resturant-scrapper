from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()

# Use Service() to handle ChromeDriver correctly
service = Service(ChromeDriverManager().install())

# Initialize WebDriver with the correct setup
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open a website
driver.get("https://www.google.com")

# Print the page title
print(driver.title)

# Close the browser
driver.quit()


