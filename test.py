import os
import random
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

load_dotenv()

# Function to sleep for a random time to mimic human behavior
def random_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
chrome_options.add_argument("--disable-media-stream")
chrome_options.add_argument("--disable-peer-to-peer")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)



# LinkedIn Login
def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    
    linkedin_username = os.getenv('LINKEDIN_USERNAME')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    username.send_keys(linkedin_username)
    password.send_keys(linkedin_password)
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    try:
        WebDriverWait(driver, 10).until(EC.url_contains('feed'))
    except:
        print("Login failed or took too long.")
        driver.quit()

# Search function to look up "laureat ensam rabat"
def search_profiles(query):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
    driver.get(search_url)
    random_sleep(3, 5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__result-container")))

# Function to extract data from each LinkedIn profile
def extract_data(profile_link):
    driver.get(profile_link)
    random_sleep(2, 4)
    
    # Extract data elements
    try:
        name = driver.find_element(By.XPATH, "//h1").text
    except:
        name = None

    try:
        degree = driver.find_element(By.XPATH, "//span[contains(text(),'Degree')]").text
    except:
        degree = None

    try:
        experience = driver.find_element(By.XPATH, "//section[contains(@class, 'experience-section')]").text
    except:
        experience = None

    try:
        skills = [skill.text for skill in driver.find_elements(By.XPATH, "//span[contains(@class, 'skill')]")]
    except:
        skills = None

    try:
        location = driver.find_element(By.XPATH, "//span[contains(@class, 'location')]").text
    except:
        location = None

    profile_data = {
        'Name': name,
        'Degree': degree,
        'Experience': experience,
        'Skills': ', '.join(skills) if skills else None,
        'Location': location,
        'Profile Link': profile_link
    }

    print(f"Data extracted for profile: {name}")
    return profile_data

# Collect data for all profiles on the search page
def collect_profiles():
    profiles_data = []
    
    # Fetch links to profiles on the search result page
    profile_links = driver.find_elements(By.XPATH, "//a[@class='app-aware-link']")
    profile_urls = [link.get_attribute('href') for link in profile_links if 'linkedin.com/in/' in link.get_attribute('href')]
    
    for url in profile_urls:
        profiles_data.append(extract_data(url))
        random_sleep(1, 2)  # Mimic human behavior

    # Save to Excel
    df = pd.DataFrame(profiles_data)
    df.to_excel("laureat_ensam_rabat_data.xlsx", index=False)

# Execute the script
linkedin_login()
search_profiles("laureat ensam rabat")
collect_profiles()

# Close the browser
driver.quit()
