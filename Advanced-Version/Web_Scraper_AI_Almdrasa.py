from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from deep_translator import GoogleTranslator
import time
import csv

# --------------------------------[ Configuration ]-----------------------------------

# Define The Path To The Zen Browser Executable:
BROWSER_PATH = r"C:\Program Files\Zen Browser\zen.exe"

# Define The Name Of The Output CSV File:
OUTPUT_FILE = 'almdrasa_courses_english.csv'

# List Of Course URLs To Scrape:
COURSE_URLS = [
    "https://almdrasa.com/tracks/programming-foundations/courses/fundamentals/",
    "https://almdrasa.com/tracks/programming-foundations/courses/beyond-the-fundamentals/",
    "https://almdrasa.com/tracks/programming-foundations/courses/python-projects/"
]

# --------------------------------[ Browser Setup ]-----------------------------------

# Initialize Firefox Options:
options = Options()

# Set The Binary Location To Zen Browser:
options.binary_location = BROWSER_PATH

# Run The Browser In Headless Mode (No GUI):
options.add_argument("--headless")

print("Initializing Scraper With Translation...")

# Setup The Driver With GeckoDriverManager:
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# Initialize The Translator (Auto Detect -> English):
translator = GoogleTranslator(source='auto', target='en')

# --------------------------------[ Helper Functions ]-----------------------------------

def safe_extract_and_translate(logic_func):
    """
    Executes a finding function safely, cleans the text, and translates it.
    """
    try:
        # Execute The Lambda Function Passed To Find The Element:
        text = logic_func()
        
        # Clean The Text By Removing Specific Arabic Phrases And Newlines:
        clean_text = text.replace(" - منصة المدرسة", "").replace("\n", " ").strip()
        
        # Translate The Cleaned Text To English:
        return translator.translate(clean_text)
        
    except Exception:
        # Return 'N/A' If Element Not Found or Translation Fails:
        return "N/A"

def get_course_details(url):
    """
    Navigates to the URL and extracts course metadata.
    """
    print(f"Processing: {url}")
    
    # Open The URL And Wait For Page Load:
    driver.get(url)
    time.sleep(5)
    
    # Extract Data Using The Safe Function With Lambda Logic:
    return {
        'Title': safe_extract_and_translate(lambda: driver.find_element(By.XPATH, "//meta[@property='og:title']").get_attribute("content")),
        'Instructor': safe_extract_and_translate(lambda: driver.execute_script("return arguments[0].textContent;", driver.find_element(By.CSS_SELECTOR, ".author-name"))),
        'Description': safe_extract_and_translate(lambda: driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content"))[:150] + "...",
        'URL': url
    }

# --------------------------------[ Main Execution ]-----------------------------------

try:
    # Open The CSV File For Writing With UTF-8-SIG Encoding (Excel Friendly):
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8-sig') as file:

        # Define The CSV Column Headers:
        fieldnames = ['Title', 'Instructor', 'Description', 'URL']
        
        # Initialize The CSV Writer:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write The Header Row:
        writer.writeheader()

        # Loop Through Each URL In The Configuration List:
        for link in COURSE_URLS:
            
            # Extract Details For The Current Course:
            details = get_course_details(link)
            
            # Write The Data Row To The CSV File:
            writer.writerow(details)
            
            print(f"Extracted: {details['Title']}")

    print(f"\nSuccess! Saved To '{OUTPUT_FILE}'")

except Exception as e:
    # Print Any Critical Errors That Occur During Execution:
    print(f"Error: {e}")

finally:
    # Close The Browser Driver Properly:
    driver.quit()
    print("Driver Closed.")