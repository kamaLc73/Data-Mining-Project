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

def random_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

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

def extract_data(profile_link):
    driver.get(profile_link)
    random_sleep(2, 4)
    
    try:
        name = driver.find_element(By.XPATH, "//h1").text
    except:
        name = "N/A"
    try:
        degree = driver.find_element(By.XPATH, "//span[contains(text(),'Degree')]").text
    except:
        degree = "N/A"
    try:
        experience = driver.find_element(By.XPATH, "//section[contains(@class, 'experience-section')]").text
    except:
        experience = "N/A"
    try:
        skills = [skill.text for skill in driver.find_elements(By.XPATH, "//span[contains(@class, 'skill')]")]
    except:
        skills = []
    try:
        location = driver.find_element(By.XPATH, "//span[contains(@class, 'location')]").text
    except:
        location = "N/A"

    profile_data = {
        'Name': name,
        'Degree': degree,
        'Experience': experience,
        'Skills': ', '.join(skills) if skills else "N/A",
        'Location': location,
        'Profile Link': profile_link
    }

    print(f"Data extracted for profile: {profile_data}")
    return profile_data

def search_profiles(query):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
    driver.get(search_url)
    random_sleep(3, 5)
    
    # Wait and ensure the search results have loaded
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__result-container")))
        print("Search results page loaded.")
    except:
        print("Failed to load search results page.")
        return

    # Print page source for debugging
    print(driver.page_source)  # Debugging: to view the page HTML structure

def collect_profiles():
    profiles_data = []
    
    # Attempt to collect profile links with refined XPaths
    profile_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
    profile_urls = [link.get_attribute('href') for link in profile_links if 'linkedin.com/in/' in link.get_attribute('href')]

    print("Collected profile URLs:", profile_urls)  # Debugging: Check profile URLs

    if not profile_urls:
        print("No profile URLs found. Adjust XPath or check page structure.")
        return

    for url in profile_urls:
        profile_data = extract_data(url)
        profiles_data.append(profile_data)
        random_sleep(1, 2)  # Mimic human behavior

    # Save to Excel if any profiles were processed
    if profiles_data:
        df = pd.DataFrame(profiles_data)
        df.to_excel("laureat_ensam_rabat_data.xlsx", index=False)
        print("Data saved successfully.")
    else:
        print("No profile data extracted.")

# Execute updated functions
linkedin_login()
search_profiles("laureat ensam rabat")
collect_profiles()

driver.quit()
