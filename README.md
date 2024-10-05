# Web Scraping Tool

This is a web scraping tool designed to collect data from any website. It uses Selenium WebDriver to navigate web pages and extract content based on specified CSS selectors. The scraped content is saved to an output file in a system-agnostic way.

## Requirements

- Python 3.6+
- Selenium
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** The `requirements.txt` file contains:

   ```
   selenium
   ```

3. **Download ChromeDriver:**

   - **Find Your Chrome Version:**
     - Open Google Chrome.
     - Click on the three vertical dots in the top-right corner.
     - Go to **Help** > **About Google Chrome**.
     - Note the version number (e.g., 96.0.4664.45). Use the major version number (e.g., 96).
   - **Download Matching ChromeDriver:**
     - Visit the [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads) page.
     - Click on the version that matches your Chrome browser's major version.
     - Download the appropriate driver for your operating system.
   - **Install ChromeDriver:**
     - Extract the downloaded ZIP file.
     - Place the `chromedriver` executable in a known directory.
     - **Windows Users:** You can place it in a folder like `C:\chromedriver\chromedriver.exe`.
     - **macOS/Linux Users:** You can place it in `/usr/local/bin/chromedriver` or another directory of your choice.
   - **Update Script Path:**
     - In `scraper.py`, update the `chromedriver_path` variable with the path to the `chromedriver` executable.

## Usage

1. **Edit the `scraper.py` Script:**

   - Open `scraper.py` in a text editor.
   - Modify the following variables near the top of the script:

     ```python
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
     ```

   - **Explanation of Variables:**

     - `base_url`: The base URL of the website you want to scrape.
     - `output_file`: The path to the file where scraped data will be saved.
     - `selectors`: A list of CSS selectors to identify the elements you want to scrape.
     - `patterns`: URL patterns with placeholders (e.g., `{num}`) to generate multiple URLs.
     - `chromedriver_path`: The file path to the `chromedriver` executable on your system.

2. **How to Choose CSS Selectors:**

   - **Open Developer Tools:**
     - Open the website you want to scrape in Chrome.
     - Navigate to a page that contains the content you are interested in.
     - Press `F12` or right-click on the page and select **Inspect** to open the Developer Tools.
   - **Inspect Elements:**
     - Use the **Element Selector** tool (an icon of a mouse cursor over a square) located at the top-left of the Developer Tools panel.
     - Click on the content you want to scrape on the webpage.
   - **Copy CSS Selector:**
     - The corresponding HTML element will be highlighted in the Elements panel.
     - Right-click on the highlighted HTML code.
     - Choose **Copy** > **Copy selector**.
   - **Paste Selector into Script:**
     - Paste the copied selector into the `selectors` list in `scraper.py`.
   - **Generalize Selectors:**
     - Be cautious if the selector includes unique IDs or classes (e.g., `#unique-id`).
     - You may need to generalize the selector to match similar elements across different pages.
     - For example, if the selector is `div.article-content`, and you notice that all articles use this class, you can use `.article-content` as your selector.

3. **Running the Script:**

   - Ensure that the `chromedriver_path` variable points to the correct location of the `chromedriver` executable.
   - Open a terminal or command prompt in the directory containing `scraper.py`.
   - Run the script:

     ```bash
     python scraper.py
     ```

4. **Understanding the Output:**

   - The scraped content will be saved in the file specified by `output_file`.
   - Each entry includes the URL and the extracted content, separated by lines for readability.
   - Logs will be printed to the console, indicating the progress of the scraping process.

## Notes

- **Random Delays:**
  - The script introduces random delays between page loads to mimic human behavior and reduce the risk of being blocked by websites.
  - You can adjust the delay range in the `random_delay` function:

    ```python
    def random_delay(min_delay=1, max_delay=3):
        time.sleep(random.uniform(min_delay, max_delay))
    ```

- **Respect Website Policies:**
  - Ensure you have permission to scrape the target website.
  - Check the website's `robots.txt` file and terms of service to understand any restrictions.

- **Adjusting URL Patterns:**
  - Modify the range in the `generate_urls` function to scrape more or fewer pages:

    ```python
    for i in range(1, 101):  # Adjust range as needed
        url = base_url + pattern.format(num=i)
        urls.append(url)
    ```

- **Scraping Specific URLs:**
  - If you have a list of specific URLs to scrape, you can bypass patterns:

    ```python
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        # Add more URLs as needed
    ]
    ```

    - Then, pass `urls` directly to `scrape_and_save_content`.

- **Headless Mode:**
  - To run the browser without opening a window (background mode), uncomment the following line in `scraper.py`:

    ```python
    options.add_argument("--headless")
    ```

## Troubleshooting

- **Common Errors:**
  - **SessionNotCreatedException:** This usually means the `chromedriver` version does not match your Chrome browser version.
    - Ensure that you have downloaded the correct version of ChromeDriver.
  - **WebDriverException:** The script cannot find the `chromedriver` executable.
    - Verify the `chromedriver_path` is correct.
  - **ElementNotInteractableException:** The script cannot find or interact with an element.
    - Check your CSS selectors and make sure they are correct.

- **Logging:**
  - The script uses Python's `logging` module to provide detailed output.
  - Adjust the logging level if you need more or less verbosity.

    ```python
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    ```

    - Levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

---

**Instructions:**

1. **Setup:**

   - Ensure you have Python 3.6 or higher installed.
   - Install dependencies using `pip install -r requirements.txt`.
   - Ensure Google Chrome is installed on your system.
   - Download the ChromeDriver that matches your Chrome version.
   - Update the `chromedriver_path` variable in `scraper.py` with the path to your `chromedriver` executable.

2. **Editing the Script:**

   - Set the `base_url` to the website you want to scrape.
   - Update the `output_file` with the desired output file path.
   - Determine the CSS selectors for the content you wish to extract (see "How to Choose CSS Selectors" above).
   - Adjust the `patterns` to match the URL patterns of the pages you want to scrape.

3. **Running the Script:**

   - Run `python scraper.py` from your terminal or command prompt.
   - The script will navigate through the generated URLs and scrape the content specified by the selectors.
   - The output will be saved to the specified `output_file`.

4. **Reviewing the Output:**

   - Open the `output_file` to review the scraped content.
   - Ensure that the data collected meets your expectations.
   - If necessary, refine your CSS selectors or URL patterns and rerun the script.
