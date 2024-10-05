# Web Scraping Tool

This is a web scraping tool designed to collect data from any website. It uses Selenium WebDriver to navigate web pages and extract content based on specified CSS selectors. The scraped content is saved to an output file in a system-agnostic way.

## Requirements

- Python 3.6+
- Selenium
- webdriver-manager
- Google Chrome browser
   ```

## Usage

Run the script with the necessary arguments:

```bash
python scraper.py --base-url BASE_URL --selectors SELECTORS --output-file OUTPUT_FILE [OPTIONS]
```

### Required Arguments

- `--base-url BASE_URL`: The base URL to scrape.
- `--selectors SELECTORS`: List of CSS selectors to locate content on the page.
- `--output-file OUTPUT_FILE`: Path to the output file where scraped content will be saved.

### Optional Arguments

- `--patterns PATTERNS`: List of URL patterns with optional placeholders (e.g., `{num}`). Example: `page/{num}`.
- `--urls URLS`: List of full URLs to scrape.
- `--chrome-driver-path CHROME_DRIVER_PATH`: Path to the ChromeDriver executable. If not provided, `webdriver-manager` will automatically manage it.
- `--headless`: Run the browser in headless mode (without a GUI).

### Examples

#### Scrape Pages Generated from Patterns

```bash
python scraper.py \
    --base-url https://example.com/ \
    --patterns "page/{num}" \
    --selectors ".content" \
    --output-file output.txt
```

This will generate URLs like `https://example.com/page/1`, `https://example.com/page/2`, ..., and scrape the content from the `.content` selector on each page.

#### Scrape Specific URLs

```bash
python scraper.py \
    --base-url https://example.com/ \
    --urls https://example.com/page1 https://example.com/page2 \
    --selectors ".content" \
    --output-file output.txt
```

This will scrape the content from the specified URLs.

## Notes

- The script introduces random delays between page loads to mimic human behavior and avoid being blocked by websites.
- Ensure you have permission to scrape the target website, adhering to its `robots.txt` file and terms of service.

**Instructions:**

1. **Setup:**
   - Make sure you have Python 3.6 or higher installed.
   - Install dependencies using `pip install -r requirements.txt`.
   - Ensure Google Chrome is installed on your system.

2. **Running the Script:**
   - Determine the base URL of the website you want to scrape.
   - Identify the CSS selectors for the content you wish to extract.
   - Decide whether to use specific URLs or generate them using patterns.
   - Run the script using the examples provided, modifying arguments as needed.

3. **Understanding the Output:**
   - The scraped content will be saved in the specified output file.
   - Each entry includes the URL and the extracted content, separated by lines for readability.

4. **Customization:**
   - Adjust the random delay range in the `random_delay` function if needed.
   - Modify the URL generation logic in `generate_urls` for more complex patterns.
   - Update selectors or add additional logic to `scrape_content` to handle different types of web content.
