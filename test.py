import os
from dotenv import load_dotenv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

load_dotenv()

def random_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# LinkedIn Login URL
driver.get('https://www.linkedin.com/login')

# Login using environment variables
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')

linkedin_username = os.getenv('LINKEDIN_USERNAME')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

username.send_keys(linkedin_username)
password.send_keys(linkedin_password)

# Click login button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Wait for login to complete
try:
    WebDriverWait(driver, 10).until(EC.url_contains('feed'))
except:
    print("Login failed or took too long.")
    driver.quit()

# Data file setup
data_file = 'graduate_data.xlsx'
if os.path.exists(data_file):
    df_existing = pd.read_excel(data_file)
else:
    df_existing = pd.DataFrame(columns=['Name', 'Degree', 'Graduation Year', 'Experience', 'Skills', 'Location', 'Profile Link'])

def extract_data(profile_link):
    driver.get(profile_link)
    random_sleep(2, 4)

    # Scrape data based on project requirements
    try:
        name = driver.find_element(By.XPATH, "//h1").text
        degree = driver.find_element(By.XPATH, "//span[contains(text(),'Degree')]").text
        experience = driver.find_element(By.XPATH, "//section[contains(@class, 'experience-section')]").text
        skills = [skill.text for skill in driver.find_elements(By.XPATH, "//span[contains(@class, 'skill')]")]
        location = driver.find_element(By.XPATH, "//span[contains(@class, 'location')]").text
    except:
        return

    profile_data = {
        'Name': name,
        'Degree': degree,
        'Graduation Year': 'Unknown',  # Placeholder if unable to extract
        'Experience': experience,
        'Skills': ', '.join(skills),
        'Location': location,
        'Profile Link': profile_link
    }

    df_existing = pd.concat([df_existing, pd.DataFrame([profile_data])]).drop_duplicates('Profile Link')
    df_existing.to_excel(data_file, index=False)

# Main scraping loop (example for a few profiles)
profile_links = ['https://www.linkedin.com/in/example1', 'https://www.linkedin.com/in/example2']  # Example links
for link in profile_links:
    extract_data(link)

# Close the browser
driver.quit()
