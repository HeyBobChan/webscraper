import re
import time
import random
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_delay(min_delay=1, max_delay=3):
    """Sleep for a random amount of time between min_delay and max_delay seconds."""
    time.sleep(random.uniform(min_delay, max_delay))

def wait_for_dynamic_content(driver, timeout=60):
    """Wait until the page is fully loaded."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def scrape_content(driver, url, selectors):
    """Scrape content from the page using the provided selectors."""
    try:
        driver.get(url)
        logging.info(f"Navigated to: {url}")
        wait_for_dynamic_content(driver)
        random_delay()

        content_texts = []
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if not elements:
                    logging.warning(f"Selector '{selector}' not found on page {url}")
                    continue
                for element in elements:
                    content_text = element.text.strip()
                    if content_text:
                        content_texts.append(content_text)
            except Exception as e:
                logging.warning(f"Error using selector '{selector}' on page {url}: {e}")
        return content_texts
    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")
        return None

def generate_urls(base_url, patterns):
    """Generate URLs based on base_url and patterns."""
    urls = []
    for pattern in patterns:
        placeholders = re.findall(r'\{(\w+)\}', pattern)
        if placeholders:
            if 'num' in placeholders:
                for i in range(1, 101):  # Adjust range as needed
                    url = base_url + pattern.format(num=i)
                    urls.append(url)
            else:
                logging.error(f"Unsupported placeholder in pattern: {pattern}")
        else:
            urls.append(base_url + pattern)
    return urls

def scrape_and_save_content(driver, urls, selectors, output_path):
    """Scrape content from URLs and save to the output file."""
    with output_path.open("w", encoding="utf-8") as f:
        for url in urls:
            content_texts = scrape_content(driver, url, selectors)
            if content_texts:
                f.write(f"URL: {url}\n")
                for idx, content in enumerate(content_texts):
                    f.write(f"Content {idx+1}:\n{content}\n\n")
                f.write("="*50 + "\n\n")
                logging.info(f"Scraped and saved content from: {url}")
            else:
                logging.info(f"No content found on: {url}")

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Base URL of the website you want to scrape
    base_url = "https://example.com/"

    # Output file path where the scraped content will be saved
    output_file = "output.txt"

    # List of CSS selectors to locate the content you want to extract
    selectors = [".content", ".article"]

    # URL patterns to generate the pages you want to scrape
    patterns = ["page/{num}"]

    # Path to your chromedriver executable
    chromedriver_path = "/path/to/chromedriver"  # Update this path

    # Prepare output path
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Setup Chrome options
    options = Options()
    options.add_argument("--incognito")
    # Uncomment the next line to run in headless mode
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize WebDriver with options
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Generate URLs
        urls = generate_urls(base_url, patterns)

        scrape_and_save_content(driver, urls, selectors, output_path)
        logging.info(f"Scraping completed. Content saved to {output_file}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
