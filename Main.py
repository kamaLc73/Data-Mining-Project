import os
from dotenv import load_dotenv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from getpass import getpass


load_dotenv()

# Function to sleep for a random amount of time between min_time and max_time
def random_sleep(min_time=1, max_time=3):
    """Sleep for a random amount of time between min_time and max_time."""
    time.sleep(random.uniform(min_time, max_time))

# Setup Selenium WebDriver
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    # Add more user agents as needed
]
user_agent = random.choice(user_agents)

chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
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

time.sleep(8)

# Wait for login to complete
try:
    WebDriverWait(driver, 10).until(EC.url_contains('feed'))
except:
    print("Login failed or took too long.")
    driver.quit()  # Exit if login fails

# Load or create the Excel file to store data
excel_file = 'information.xlsx'

if os.path.exists(excel_file):
    df_existing = pd.read_excel(excel_file)
else:
    df_existing = pd.DataFrame(columns=['Name', 'Bio', 'Company', 'Phone Number', 'Email', 'Profile Link'])

# Function to navigate and interact with the first page before connections
def initial_navigation():
    """Perform some initial navigation before going to the connections page."""
    driver.get('https://www.linkedin.com/feed/')
    random_sleep(5, 10)  # Random delay to mimic human behavior
    
    driver.get('https://www.linkedin.com/search/results/people/')
    random_sleep(5, 10)  # Random delay

initial_navigation()

# Open the LinkedIn connections page and wait for it to load
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
random_sleep(5, 10)  # Random delay

# Initialize an empty list to store the scraped data
data = []
visited_links = []  # Track visited links during the session
page_count = 0  # Track the number of pages processed

def re_login():
    """Logs out and logs back in to avoid detection."""
    driver.get('https://www.linkedin.com/logout/')
    random_sleep(5, 10)
    
    driver.get('https://www.linkedin.com/login')
    random_sleep(5, 10)
    
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    
    linkedin_username = os.getenv('LINKEDIN_USERNAME')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    username.send_keys(linkedin_username)
    password.send_keys(linkedin_password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    random_sleep(5, 10)

def load_all_connections():
    """Scrolls down and clicks 'Afficher plus de résultats' until all connections are loaded"""
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2, 4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2, 4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            random_sleep(2, 4)
            show_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Afficher plus de résultats']"))
            )
            ActionChains(driver).move_to_element(show_more_button).perform()
            random_sleep(1, 2)
            show_more_button.click()
            random_sleep(2, 4)
        except:
            print("No more 'Afficher plus de résultats' buttons found. Continuing scrolling...")
            break

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2, 4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page. No more content to load.")
            break
        last_height = new_height

def extract_profile_data(profile_link):
    """Extracts data from an individual LinkedIn profile"""
    driver.execute_script(f"window.open('{profile_link}');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
    random_sleep(2, 4)
    
    try:
        name = driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]").text
    except:
        name = None
    
    try:
        bio = driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium')]").text
    except:
        bio = None
    
    try:
        company = driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[3]/div[3]/ul/li[1]/div/div[2]/div[1]/div/span[1]/span[1]/text()").text
    except:
        try:
            company = driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li/button/span/div/text()").text
        except:
            company = None

    try:
        contact_button = driver.find_element(By.XPATH, "//a[@id='top-card-text-details-contact-info']")
        contact_button.click()
        random_sleep(2, 4)
        
        try:
            phone_number = driver.find_element(By.XPATH, "//span[contains(@class, 't-14 t-black t-normal')]").text
        except:
            phone_number = None
        
        try:
            email = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]").get_attribute('href').replace('mailto:', '')
        except:
            email = None
    except:
        phone_number = None
        email = None

    profile_data = {
        'Name': name,
        'Bio': bio,
        'Company': company,
        'Phone Number': phone_number,
        'Email': email,
        'Profile Link': profile_link
    }

    data.append(profile_data)
    df_new = pd.DataFrame(data)
    
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['Profile Link'], keep='last')
    
    df_combined.to_excel(excel_file, index=False)
    
    print(f"Profile data saved: {profile_data['Name']}")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def process_connections_page():
    """Processes all connections on the current page in order"""
    global page_count
    load_all_connections()
    
    followers = driver.find_elements(By.XPATH, "//a[@class='ember-view mn-connection-card__link']")
    profile_links = [follower.get_attribute('href') for follower in followers]
    
    last_profile_link = None
    
    for profile_link in profile_links:
        if profile_link in visited_links or profile_link == last_profile_link:
            print(f"Profile already visited or duplicate: {profile_link}")
            continue
        
        if not df_existing[df_existing['Profile Link'] == profile_link].empty:
            print(f"Profile already exists in file: {profile_link}")
            continue
        
        extract_profile_data(profile_link)
        visited_links.append(profile_link)
        last_profile_link = profile_link
    
    page_count += 1
    if page_count >= 10:
        re_login()
        page_count = 0

# Start the process
process_connections_page()

# Close the browser when finished
driver.quit()