import requests
from bs4 import BeautifulSoup

# --------------------------------[ Configuration ]-----------------------------------

# Enter The Target URL You Want To Scrape Here:
url = "https://books.toscrape.com/"

# --------------------------------[ HTTP Request ]-----------------------------------

# Send A GET Request To Fetch The Raw HTML Content:
response = requests.get(url)

# Parse The HTML Content Using BeautifulSoup:
soup = BeautifulSoup(response.content, "html.parser")

# --------------------------------[ Data Extraction ]-----------------------------------

# Find All Book Containers (HTML Articles With Class 'product_pod'):
books = soup.find_all("article", class_="product_pod")

# Loop Through Each Book Container To Extract Specific Details:
for book in books:
    
    # Extract The Full Title From The 'title' Attribute Inside The <a> Tag:
    title = book.h3.a["title"]
    
    # Extract The Rating Class Name (E.g., 'Three', 'Four'):
    rating = book.p["class"][1]
    
    # Extract The Price Text From The <p> Tag With Class 'price_color':
    price = book.find("p", class_="price_color").text
    
    # Display The Extracted Data In A Readable Format:
    print(f"Book: {title} | Rating: {rating} Stars | Price: {price}")