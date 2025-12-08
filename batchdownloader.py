from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import requests
import time
import sys

# --- Configuration ---
# 1. REPLACE THIS with the URL of the episode list page.
PAGE_URL = "YOUR_EPISODE_LIST_URL_HERE" 
# 2. REPLACE THIS with the absolute path to your desired download directory.
DOWNLOAD_DIR = "YOUR_ABSOLUTE_DOWNLOAD_PATH_HERE" 

# --- Core Functions ---

def get_download_links_selenium(url):
    """
    Uses Selenium (headless browser) to render the page and extract 
    (filename, download_link) tuples, bypassing anti-bot measures.
    """
    print("--- Starting Headless Browser (Selenium) ---")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        # Wait for JavaScript content to load
        time.sleep(5) 
        
        page_source = driver.page_source
        
    except Exception as e:
        print(f"FATAL ERROR during Selenium operation: {e}")
        print("Ensure Google Chrome is installed and required libraries are up to date.")
        return []
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Browser session closed.")

    # --- BeautifulSoup Parsing on Rendered Content ---
    soup = BeautifulSoup(page_source, 'html.parser')
    download_data = [] # Stores (filename, download_url) tuples
    
    # Target the container for each episode: <div class="list-group-item list-group-item-action">
    episode_containers = soup.find_all('div', class_='list-group-item list-group-item-action')
    
    if not episode_containers:
        return []

    print(f"Found {len(episode_containers)} episode containers.")

    for container in episode_containers:
        # 1. Extract the Clean Filename (from the episode title link)
        title_tag = container.find('a', attrs={'view': True})
        
        if not title_tag:
            all_a_tags = container.find_all('a')
            if all_a_tags:
                title_tag = max(all_a_tags, key=lambda tag: len(tag.text.strip()), default=None)

        clean_filename = None
        if title_tag:
            raw_title = title_tag.text.strip()
            # Clean filename by replacing unsafe characters
            clean_filename = raw_title.replace('/', '_').replace(':', ' -')
            if not clean_filename.lower().endswith('.mkv'):
                clean_filename = f"{clean_filename}.mkv"
        
        if not clean_filename:
            continue 

        # 2. Extract the Download URL 
        # Target the <a> tag that contains the 'download.aspx?file='
        download_tag = container.find('a', href=lambda href: href and 'download.aspx?file=' in href)

        if download_tag:
            download_url = download_tag['href']
            download_data.append((clean_filename, download_url))
            
    return download_data


def download_file(filename, url, download_dir):
    """Downloads a single file from a given URL using the requests library."""
    
    filepath = os.path.join(download_dir, filename)

    if os.path.exists(filepath):
        print(f"File already exists: {filename}. Skipping.")
        return

    print(f"Starting download for: {filename}")
    try:
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
    if PAGE_URL == "YOUR_EPISODE_LIST_URL_HERE" or DOWNLOAD_DIR == "YOUR_ABSOLUTE_DOWNLOAD_PATH_HERE":
        print("🚨 Please update PAGE_URL and DOWNLOAD_DIR in the script configuration.")
        sys.exit(1)
        
    DOWNLOAD_DIR = os.path.expanduser(DOWNLOAD_DIR)
    
    print("Script execution started.")
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created download directory: {DOWNLOAD_DIR}")

    # 1. Get the list of (filename, download_url) tuples
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