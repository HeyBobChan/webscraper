import re
import time
import random
import argparse
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# For automatic driver management
from webdriver_manager.chrome import ChromeDriverManager

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
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                content_text = element.text.strip()
                content_texts.append(content_text)
            except Exception:
                logging.warning(f"Selector '{selector}' not found on page {url}")
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
                for i in range(1, 100):  # Adjust range as needed
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

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Web scraping script to extract data from a website.")
    parser.add_argument('--base-url', type=str, required=True, help='The base URL to scrape.')
    parser.add_argument('--output-file', type=str, required=True, help='Output file path.')
    parser.add_argument('--patterns', type=str, nargs='+', help='List of URL patterns with optional placeholders.')
    parser.add_argument('--selectors', type=str, nargs='+', required=True, help='List of CSS selectors to locate content.')
    parser.add_argument('--chrome-driver-path', type=str, help='Path to chromedriver executable.')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode.')
    parser.add_argument('--urls', type=str, nargs='+', help='List of full URLs to scrape.')

    args = parser.parse_args()

    base_url = args.base_url
    output_file = args.output_file
    patterns = args.patterns
    selectors = args.selectors
    chrome_driver_path = args.chrome_driver_path
    headless = args.headless
    urls = args.urls

    # Validate arguments
    if not urls and not patterns:
        logging.error("You must provide either a list of URLs or patterns to generate URLs.")
        exit(1)

    # Prepare output path
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Setup Chrome options
    options = Options()
    options.add_argument("--incognito")
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize WebDriver with options
    if chrome_driver_path:
        service = Service(chrome_driver_path)
    else:
        # Use webdriver-manager to handle driver
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Generate URLs if patterns are provided
        if patterns:
            url_list = generate_urls(base_url, patterns)
        else:
            url_list = urls

        scrape_and_save_content(driver, url_list, selectors, output_path)
        logging.info(f"Scraping completed. Content saved to {output_file}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
