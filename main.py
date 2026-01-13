import requests
from bs4 import BeautifulSoup

# Fetch the title of example.com
url = "https://example.com"

try:
    # Send GET request
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for bad status codes
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else "No title found"
    
    print(f"Website: {url}")
    print(f"Title: {title}")
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching website: {e}")

