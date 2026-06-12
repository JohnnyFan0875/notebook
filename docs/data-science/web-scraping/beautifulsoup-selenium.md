# Python Web Scraping

Web scraping allows you to extract and process information from websites. Two of the most common approaches in Python are:

- **BeautifulSoup** (parsing static HTML)
- **Selenium** (interacting with dynamic websites)

## BeautifulSoup Example

```python
from bs4 import BeautifulSoup
import requests

# Fetch HTML from a website
html_text = requests.get('<website>').text
soup = BeautifulSoup(html_text, 'lxml')

# Save parsed HTML
with open('output_html', 'w', encoding='utf-8') as soup_output:
    soup_output.write(str(soup))

# Load HTML from file
with open('<html>', 'r', encoding='utf-8') as html_input:
    content = html_input.read()
    soup = BeautifulSoup(content, 'lxml')

    # Find all tags
    tag_li = soup.find_all('<tag>')  # returns list

    # Find divs with specific class
    tags_div_class_name_li = soup.find_all('div', class_='<keyword>')
    for tags_div_class_name in tags_div_class_name_li:
        tag_h1 = tags_div_class_name.h1
        tag_h1_name = tags_div_class_name.h1.text     # tag text
        tag_h1_attr = tags_div_class_name.h1['href']  # attribute
        sub_tag_li = tags_div_class_name.find_all('h1', class_='<keyword>')
```

### Notes

- Use `.prettify()` to format HTML for better readability.
- Use `.text` to extract text inside tags.
- Attributes can be accessed like dictionaries, e.g., `tag['href']`.

## Selenium Example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time as t
import random

chrome = webdriver.Chrome(ChromeDriverManager().install())
chrome.get('https://browserleaks.com/ip')

t.sleep(random.randint(5))

# Find element by ID
element_id = chrome.find_element(By.ID, '<keyword>')  # first match
elements_id = chrome.find_elements(By.ID, '<keyword>')  # all matches (list)

# Explicit waits
# Check if a single element exists in HTML
element_id = WebDriverWait(chrome, 10).until(
    EC.presence_of_element_located((By.ID, '<keyword>')),
    'Cannot find the element.'
)

# Check if at least one matching element exists
element_id = WebDriverWait(chrome, 10).until(
    EC.presence_of_all_elements_located((By.ID, '<keyword>')),
    'Cannot find the elements.'
)

# Check if an element is clickable (visible + enabled)
element_clickable = WebDriverWait(chrome, 10).until(
    EC.element_to_be_clickable((By.ID, '<keyword>')),
    'Cannot click the element.'
)

element_clickable.send_keys('<send_information>')
element_clickable.click()

chrome.close()   # close just one window/tab
# chrome.quit()  # shut down the whole browser and end the session
```

### About `element_to_be_clickable`

- Ensures the element is both **visible** and **enabled** before interacting with it.
- Prevents errors where an element exists but is covered by another element, hidden, or disabled.
- Usage pattern:

  ```python
  clickable_elem = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.ID, 'submit-button'))
  )
  clickable_elem.click()
  ```

## XPath for Precise Location

```html
<html>
  <body>
    <form id="loginForm">
      <input name="username" type="text" />
      <input name="password" type="password" />
      <input name="continue" type="submit" value="Login" />
      <input name="continue" type="button" value="Clear" />
    </form>
  </body>
</html>
```

```python
username = driver.find_element_by_xpath("//form[@id='loginForm']/input[1]")
clear_button = driver.find_element_by_xpath("//input[@name='continue'][@type='button']")
```

## Selenium with Custom Headers (User-Agent)

```python
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent_li = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    # Add more User-Agent strings as needed
]

options = Options()
random_user_agent = random.choice(user_agent_li)
options.add_argument(f"--user-agent={random_user_agent}")
options.add_argument('--disable-notifications')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--start-maximized')
options.add_argument('--incognito')

chrome = webdriver.Chrome(options=options)
chrome.get('<url>')

chrome.quit()
```

## Best Practices

- **Respect website policies**: Always check a site’s robots.txt and terms of service.
- **Throttle requests**: Add delays (`time.sleep`) or random intervals to avoid overloading servers.
- **Use headers**: Randomize `User-Agent` strings to simulate real browser traffic.
- **Avoid detection**: Use Selenium stealth modes and proxies if necessary.
- **Data cleaning**: Combine scraping with libraries like `pandas` for structured analysis.

This guide covers **BeautifulSoup** for static HTML and **Selenium** for dynamic content, with consistent examples and tips for safe, effec
