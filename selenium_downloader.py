from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import requests
import time
import sys

print(f"Script started ")
# --- Configuration ---
# 1. Page URL (The episode list page)
PAGE_URL = "https://worker-wispy-night-f30b.kayoanime108.workers.dev/0:/SEASON%202/" 
# 2. Download Directory (Ensure this path is where you want files saved)
DOWNLOAD_DIR = "/Users/chiragdahiya/Enjoyment/Anime/My Hero Academia/S02" 

# --- Core Functions ---

def get_download_links_selenium(url):
    """
    Uses Selenium to bypass anti-bot measures, get rendered HTML, 
    and extract (filename, link) tuples.
    """
    print("--- Starting Headless Browser (Selenium) ---")
    
    # Configure Chrome options to run in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        # Automatically download/locate the correct Chrome Driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("Chrome Driver successfully initialized.")
        
        driver.get(url)
        print(f"Browser navigated to: {url}")
        
        # Wait for JavaScript content to load
        time.sleep(5) 
        
        page_source = driver.page_source
        
    except Exception as e:
        print(f"FATAL ERROR during Selenium operation: {e}")
        print("Ensure Google Chrome is installed and updated.")
        return []
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Browser session closed.")

    # --- BeautifulSoup Parsing on Rendered Content ---
    soup = BeautifulSoup(page_source, 'html.parser')
    download_data = [] # Stores (filename, download_url) tuples
    
    print("Parsing rendered HTML for episode containers...")
    
    # Target the container for each episode: <div class="list-group-item list-group-item-action">
    episode_containers = soup.find_all('div', class_='list-group-item list-group-item-action')
    
    if not episode_containers:
        print("ALERT: Found 0 episode containers. Site structure may have changed.")
        return []

    print(f"Found {len(episode_containers)} episode containers.")

    for container in episode_containers:
        # 1. Extract the Clean Filename (from the episode title link)
        # We look for the anchor tag containing the visible title.
        title_tag = container.find('a', attrs={'view': True})
        
        if not title_tag:
            # Fallback: try to find the <a> tag with the longest text (usually the title)
            all_a_tags = container.find_all('a')
            if all_a_tags:
                title_tag = max(all_a_tags, key=lambda tag: len(tag.text.strip()), default=None)

        clean_filename = None
        if title_tag:
            raw_title = title_tag.text.strip()
            # Ensure safe filename and extension
            clean_filename = raw_title.replace('/', '_').replace(':', ' -')
            if not clean_filename.lower().endswith('.mkv'):
                clean_filename = f"{clean_filename}.mkv"
        
        if not clean_filename:
             # Skip this item if no title could be determined
            continue 

        # 2. Extract the Download URL 
        # Target the <a> tag that contains the 'download.aspx?file='
        download_tag = container.find('a', href=lambda href: href and 'download.aspx?file=' in href)

        if download_tag:
            download_url = download_tag['href']
            download_data.append((clean_filename, download_url))
        else:
            # If we found a title but no link, something is wrong, skip it.
            print(f"Warning: Found title '{clean_filename}' but no matching download link. Skipping.")
            
    return download_data


def download_file(filename, url, download_dir):
    """Downloads a single file from a given URL using the requests library."""
    
    filepath = os.path.join(download_dir, filename)

    if os.path.exists(filepath):
        print(f"File already exists: {filename}. Skipping download.")
        return

    print(f"Starting download for: {filename}")
    try:
        # Use headers to ensure the download stream looks like a regular request
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Stream the download
        with requests.get(url, stream=True, timeout=300, headers=headers) as r:
            r.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: 
                        f.write(chunk)

        print(f"Successfully downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

# --- Main Execution ---

if __name__ == "__main__":
    # Expand the home directory symbol (~) if it was used
    DOWNLOAD_DIR = os.path.expanduser(DOWNLOAD_DIR)
    
    print("Script execution started.")
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created download directory: {DOWNLOAD_DIR}")

    # 1. Get the list of (filename, download_url) tuples using Selenium
    download_data = get_download_links_selenium(PAGE_URL)

    if not download_data:
        print("\n❌ No download data found. Aborting downloads.")
    else:
        print(f"\n✅ Found {len(download_data)} unique download links with names.")
        print("-" * 30)

        # 2. Iterate through the tuples and download files
        for filename, link in download_data:
            download_file(filename, link, DOWNLOAD_DIR)
        
        print("-" * 30)
        print("✨ All download attempts complete.")