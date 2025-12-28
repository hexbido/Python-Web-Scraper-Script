import requests
from bs4 import BeautifulSoup

# --------------------------------[ Configuration ]-----------------------------------

# Enter The Target URL To Scrape Here:
TARGET_URL = "https://books.toscrape.com/"

# Set The Maximum Time (In Seconds) To Wait For A Response:
TIMEOUT_SECONDS = 10

# --------------------------------[ Initialization ]-----------------------------------

print("Starting The Search Process...")

# --------------------------------[ Main Logic ]-----------------------------------

try:
    # Send A GET Request With The Specified Timeout:
    response = requests.get(TARGET_URL, timeout=TIMEOUT_SECONDS)
    
    # Check If The Request Was Successful (Raises Error For 4xx Or 5xx Codes):
    response.raise_for_status()
    
    # Parse The HTML Content Using BeautifulSoup:
    soup = BeautifulSoup(response.content, "html.parser")

    # Initialize A Counter For The Books:
    book_count = 1

    # --------------------------------[ Data Extraction ]-----------------------------------

    # Iterate Through Each Book Container Found By CSS Selector:
    for book in soup.select("article.product_pod"):
        try:
            # Extract The Book Title From The Anchor Tag Attribute:
            title = book.h3.a["title"]
            
            # Extract The Price And Remove The Currency Symbol (£):
            price = book.select_one(".price_color").text.replace("£", "")
            
            # Extract The Star Rating (The Second Class Name, E.g., 'Three'):
            rating = book.select_one(".star-rating")["class"][1]

            # Display The Formatted Extracted Data:
            print(f"{'-' * 15} BOOK {book_count} {'-' * 15}")
            print(f"Book:   {title}")
            print(f"Rating: {rating}")
            print(f"Price:  {price}")
            print("")

            # Increment The Book Counter:
            book_count += 1

        # Handle Cases Where Specific Data Might Be Missing In An Element:
        except (AttributeError, IndexError):
            continue

# --------------------------------[ Error Handling ]-----------------------------------

# Catch And Display Any Network Or Request-Related Errors:
except requests.exceptions.RequestException as error:
    print(f"Critical Error: {error}")