[Data Science](../README.md) › [Web Scraping](README.md) › BeautifulSoup 與 Selenium

# BeautifulSoup 與 Selenium

靜態頁用 `requests` 下載 HTML、BeautifulSoup 解析；資料要等 JavaScript 載入、或需要登入與點擊時，才用 Selenium 驅動真的瀏覽器。Selector 語法與共用原則見 [Web Scraping](README.md#共用觀念)。

| 情境 | 工具 | 速度 |
| --- | --- | --- |
| 原始 HTML 裡就有資料 | `requests` + BeautifulSoup（或 parsel，見 [Scrapy 與 Selector](scrapy-and-selectors.md)） | 快 |
| 頁面表格（`<table>`） | `pd.read_html(html)`（需 `lxml`），回傳 `list[DataFrame]` | 快 |
| 資料由 JS 產生，但 Network 有 JSON 端點 | 直接 `requests.get(json_url)` | 快 |
| 必須執行 JS、登入、點擊、捲動 | Selenium 或 Playwright | 慢（啟動整個瀏覽器） |

## BeautifulSoup：靜態頁

```python
import time
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "mylab-scraper/0.1 (me@uni.edu)"}
r = requests.get("https://example.com/courses", headers=headers, timeout=10)
r.raise_for_status()                                  # 4xx / 5xx 直接拋錯，不要解析錯誤頁
soup = BeautifulSoup(r.text, "lxml")                  # 解析器：lxml 快；"html.parser" 免安裝

# 1. 先選重複區塊，再在區塊內抓欄位
rows = []
for card in soup.select("div.course-block"):          # CSS selector，回傳 list
    link = card.select_one("a")                       # 第一個符合，找不到回傳 None
    rows.append({
        "title": link.get_text(strip=True) if link else None,   # 含所有子節點文字
        "url":   link.get("href") if link else None,            # .get() 缺屬性回傳 None；link["href"] 會 KeyError
    })

# 2. find / find_all：依標籤與屬性
soup.find("h1")                                       # 第一個
soup.find_all("div", class_="course-block")           # class 是保留字，所以參數名是 class_
soup.find_all("a", href=True)                         # 只要有 href 的 <a>
soup.find("div", attrs={"data-id": "42"})

# 3. 文字與屬性
tag = soup.select_one("p#intro")
tag.get_text(" ", strip=True)                         # 子節點間用空白分隔，去除前後空白
tag.attrs                                             # 全部屬性 dict

# 4. 相對連結 → 絕對網址
from urllib.parse import urljoin
urljoin(r.url, "/course/python")                      # https://example.com/course/python

time.sleep(1)                                         # 下一個請求前先節流
```

| 方法 | 回傳 | 說明 |
| --- | --- | --- |
| `select(css)` / `select_one(css)` | list / Tag 或 `None` | 用 CSS selector，最直覺 |
| `find_all(name, attrs)` / `find(...)` | list / Tag 或 `None` | 依標籤名與屬性 |
| `.text` / `.get_text(sep, strip=True)` | `str` | 含所有後代文字；`.string` 只在唯一子節點時有值 |
| `tag["href"]` / `tag.get("href")` | `str` | 前者缺屬性會 `KeyError` |
| `.parent`、`.find_next_sibling()` | Tag | 沿樹移動 |
| `soup.prettify()` | `str` | 排版後的 HTML，除錯用 |

> 一個區塊缺某欄位時，`select_one` 回傳 `None`，直接 `.get_text()` 會 `AttributeError`。在區塊內逐欄抓並處理 `None`，才不會讓整批因為一筆資料中斷，也不會讓欄位錯位。

除錯時把 `r.text` 存檔，之後讀檔解析，避免重複送請求：

```python
from pathlib import Path
Path("page.html").write_text(r.text, encoding="utf-8")
soup = BeautifulSoup(Path("page.html").read_text(encoding="utf-8"), "lxml")
```

## Selenium：動態頁

Selenium 4.6 起內建 Selenium Manager，會自動下載對應的瀏覽器 driver，不再需要 `webdriver_manager`。

```python
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless=new")                # 不開視窗
options.add_argument("--window-size=1920,1080")       # headless 預設視窗小，RWD 版面可能不同
options.add_argument("--user-agent=mylab-scraper/0.1 (me@uni.edu)")

driver = webdriver.Chrome(options=options)            # Selenium Manager 自動處理 chromedriver
try:
    driver.get("https://example.com/login")
    wait = WebDriverWait(driver, 10)                  # 最多等 10 秒

    # 1. 找元素：find_element(By.X, ...)；find_element_by_* 在 Selenium 4 已移除
    user = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    user.send_keys("me")
    driver.find_element(By.NAME, "password").send_keys("...")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@id='loginForm']//input[@type='submit']"))).click()

    # 2. 等資料出現再抓：明確等待 (explicit wait)，不要用固定 sleep
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#results tr")))
    data = [r.text for r in rows]

    # 3. 也可以把渲染後的 HTML 交給 BeautifulSoup 解析
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")

    time.sleep(random.uniform(1, 3))                  # 頁面之間隨機間隔 1–3 秒
finally:
    driver.quit()                                     # 結束整個瀏覽器；close() 只關目前分頁，程序會殘留
```

| 等待條件 (`EC.*`) | 成立時機 | 用途 |
| --- | --- | --- |
| `presence_of_element_located` | 元素存在於 DOM（不一定看得見） | 抓資料 |
| `visibility_of_element_located` | 存在且可見 | 讀取顯示的文字 |
| `element_to_be_clickable` | 可見且啟用 | 點擊、輸入；避免被遮住或 disabled 時操作失敗 |
| `presence_of_all_elements_located` | 至少一個符合 | 列表、表格列 |
| `text_to_be_present_in_element` | 元素內出現指定文字 | 等搜尋結果更新 |

`wait.until(...)` 逾時會拋 `TimeoutException`；第二個參數可以帶錯誤訊息，例如 `wait.until(cond, "找不到結果表格")`。

| `By` | 例子 |
| --- | --- |
| `By.ID` / `By.NAME` / `By.CLASS_NAME` | `(By.ID, "submit")` |
| `By.CSS_SELECTOR` | `(By.CSS_SELECTOR, "div.card > a")` |
| `By.XPATH` | `(By.XPATH, "//input[@name='continue'][@type='button']")` |
| `By.LINK_TEXT` | `(By.LINK_TEXT, "Next")` |

### 常用操作

| 任務 | 寫法 |
| --- | --- |
| 捲到底觸發 lazy loading | `driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")` |
| 切換到 iframe | `driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))`；回主頁 `switch_to.default_content()` |
| 截圖除錯 | `driver.save_screenshot("debug.png")` |
| 讀屬性 | `el.get_attribute("href")` |
| 選下拉選單 | `from selenium.webdriver.support.select import Select`；`Select(el).select_by_visible_text("2024")` |

> 新專案可考慮 [Playwright](https://playwright.dev/python/)：內建自動等待、可攔截網路請求直接拿 JSON，通常比 Selenium 穩。

## 常見錯誤

| 錯誤寫法 | 問題 | 正確寫法 |
| --- | --- | --- |
| `webdriver.Chrome(ChromeDriverManager().install())` | Selenium 4 第一個位置參數不是 driver 路徑 | `webdriver.Chrome()`；自訂路徑用 `service=Service("path")` |
| `driver.find_element_by_xpath(...)` | Selenium 4.3 移除 | `driver.find_element(By.XPATH, ...)` |
| `time.sleep(random.randint(5))` | `randint` 需要兩個參數，會 `TypeError` | `time.sleep(random.uniform(1, 5))` |
| 固定 `sleep(5)` 等頁面 | 太短會失敗、太長浪費時間 | `WebDriverWait` + `expected_conditions` |
| `requests.get(url)` 沒有 `timeout` | 伺服器沒回應時永遠卡住 | `requests.get(url, timeout=10)` |
| 輪換假 User-Agent 規避封鎖 | 違反多數網站條款 | 表明身分、放慢速度，或改用 API |
| `driver.close()` 收尾 | 只關分頁，chromedriver 程序殘留 | `try` / `finally` + `driver.quit()` |
