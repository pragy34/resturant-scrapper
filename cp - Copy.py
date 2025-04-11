from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (remove to see browser)
driver = webdriver.Chrome(options=options)

# Open Google Maps
driver.get("https://www.google.com/maps")
wait = WebDriverWait(driver, 10)

# Search for restaurants in Connaught Place, Delhi
service = "restaurants"
location = "Connaught Place, Delhi"
search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
search_box.send_keys(f"{service} in {location}")
search_box.send_keys(Keys.ENTER)
time.sleep(5)  # Wait for results to load

# Scroll through results
for _ in range(7):  # Increase for more results
    driver.execute_script("document.querySelector('div[role=\"feed\"]').scrollBy(0, 1000);")
    time.sleep(2)

# Find all business listings
businesses = driver.find_elements(By.CLASS_NAME, "Nv2PK")
data = []

for business in businesses[:10]:  # Adjust for more results
    try:
        # Click on the business
        business.click()
        time.sleep(3)

        # Extract details
        name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf"))).text
        address = driver.find_element(By.CLASS_NAME, "Io6YTe").text

        # Extract phone number properly
        try:
            phone_element = driver.find_element(By.XPATH, "//button[contains(@data-tooltip, 'Call')]")
            phone = phone_element.get_attribute("aria-label").replace("Call ", "").strip()
        except:
            phone = "N/A"

        # Extract rating
        try:
            rating = driver.find_element(By.CLASS_NAME, "MW4etd").text
        except:
            rating = "N/A"

        # Extract Cuisine Type
        try:
            cuisine_type = driver.find_element(By.XPATH, "//div[@class='UY7F9']").text
        except:
            cuisine_type = "N/A"

        print(f"Scraped: {name}, {address}, {phone}, {rating}, {cuisine_type}")
        data.append({"Name": name, "Address": address, "Phone": phone, "Rating": rating, "Cuisine Type": cuisine_type})

    except Exception as e:
        print(f"Error scraping: {e}")

# Save to Excel
df = pd.DataFrame(data)
df.to_excel("restaurants_data.xlsx", index=False, engine="openpyxl")

print("Scraping complete. Data saved to 'restaurants_data.xlsx'")
driver.quit()
