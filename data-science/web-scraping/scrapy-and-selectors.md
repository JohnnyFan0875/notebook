[Data Science](../README.md) › [Web Scraping](README.md) › Scrapy 與 Selector

# Scrapy 與 Selector

Scrapy 是 Python 的爬蟲框架：排程請求、跟隨連結、節流、重試、輸出都幫你處理好。它的 selector 引擎 `parsel` 也可以單獨使用，對任何 HTML 寫 CSS / XPath。CSS 與 XPath 語法對照見 [Web Scraping](README.md#css-selector-vs-xpath)。

```
抓一頁 → 解析 HTML → 選重複區塊 → 抽文字 / 屬性 → 跟隨下一頁連結 → 輸出結構化資料
```

| 規模 | 工具 |
| --- | --- |
| 一兩頁 | `requests` + `parsel.Selector`（或 BeautifulSoup） |
| 數十頁以上、需要跟隨連結、重試、節流 | Scrapy spider |

## Selector：單頁解析

```python
import requests
from parsel import Selector          # scrapy.Selector 是同一個東西

r = requests.get("https://en.wikipedia.org/wiki/Web_scraping",
                 headers={"User-Agent": "mylab-scraper/0.1 (me@uni.edu)"}, timeout=10)
r.raise_for_status()
sel = Selector(text=r.text)

# 1. 選取：回傳 SelectorList（還不是字串）
sel.xpath("//p")
sel.css("div#uid > p.class-1")

# 2. 抽值：.get() 取第一個（找不到回傳 None）、.getall() 取全部（list）
sel.css("h1::text").get()
sel.css("h1::text").get(default="NA")                # 找不到時的預設值
sel.css("a::attr(href)").getall()                    # CSS 取屬性
sel.xpath("//a/@href").getall()                      # XPath 取屬性

# 3. 直接文字 vs 所有後代文字：<p id="p-example">Hello <a>world</a>!</p>
sel.xpath('//p[@id="p-example"]/text()').getall()    # ['Hello ', '!']
sel.xpath('//p[@id="p-example"]//text()').getall()   # ['Hello ', 'world', '!']
sel.css("p#p-example::text").getall()                # ['Hello ', '!']
sel.css("p#p-example ::text").getall()               # ['Hello ', 'world', '!']（::text 前有空白 = 後代）
sel.css("p#p-example").xpath("string()").get()       # 'Hello world!'（串成一個字串）

# 4. 先選區塊，再用相對路徑抓欄位
for block in sel.css("div.course-block"):
    title = block.css("a::text").get()
    href  = block.xpath("./a/@href").get()           # ./ 從目前區塊開始；寫 //a 會回到整頁搜尋
```

| 舊 API | 新 API | 說明 |
| --- | --- | --- |
| `.extract_first()` | `.get()` | 第一個值或 `None` |
| `.extract()` | `.getall()` | 全部值的 list |
| `.re(r"...")` / `.re_first(r"...")` | 不變 | 用 regex 抽出片段 |

> 在迴圈裡用 XPath 時，`block.xpath("//a")` 的 `//` 是從**整份文件**開始，不是從 `block`；要寫 `.//a` 或 `./a`。這是區塊內抓到別人資料最常見的原因。

### XPath 常用寫法

| 寫法 | 意義 |
| --- | --- |
| `/html/body/div/p[2]` | 從根開始的絕對路徑；`[2]` 是同層第 2 個（從 1 起算） |
| `//table` | 任意位置的 `<table>` |
| `//p[@class="class-1"]` | class 完全等於 `class-1`（多 class 時會失敗） |
| `//*[contains(@class, "class-1")]` | class 字串包含（也會誤中 `class-10`） |
| `//div[@id="uid"]/p[2]` | 屬性條件 + 位置 |
| `//h1[contains(@class, "title")]/text()` | 文字 |
| `//div[a]` | 含有 `<a>` 子節點的 `div` |
| `./*` | 目前節點的所有直接子節點（摸索陌生結構時好用） |

## Scrapy Spider：多頁爬取

```python
import scrapy
from scrapy.crawler import CrawlerProcess


class CourseSpider(scrapy.Spider):
    name = "courses"
    start_urls = ["https://www.example.com/courses"]       # 取代手寫 start_requests()
    custom_settings = {
        "USER_AGENT": "mylab-scraper/0.1 (me@uni.edu)",
        "ROBOTSTXT_OBEY": True,                             # 遵守 robots.txt
        "DOWNLOAD_DELAY": 1.0,                              # 同一網域請求間隔（秒，實際會隨機 0.5–1.5 倍）
        "AUTOTHROTTLE_ENABLED": True,                       # 依伺服器回應時間自動放慢
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "HTTPCACHE_ENABLED": True,                          # 快取回應，改 selector 重跑不必重抓
        "FEEDS": {"courses.jsonl": {"format": "jsonlines"}},  # 輸出檔
    }

    def parse(self, response):
        # 列表頁：抓每門課的連結，交給 parse_course
        for href in response.css("div.course-block > a::attr(href)").getall():
            yield response.follow(href, callback=self.parse_course)   # 自動處理相對連結
        # 下一頁
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_course(self, response):
        # 詳細頁：yield dict 就是一筆輸出
        yield {
            "url": response.url,
            "title": response.xpath('//h1[contains(@class, "title")]/text()').get(default="").strip(),
            "chapters": response.css("h4.chapter__title::text").getall(),
        }


process = CrawlerProcess()
process.crawl(CourseSpider)
process.start()                                             # 阻塞直到爬完；同一個 Python 程序只能 start 一次
```

| 元件 | 角色 |
| --- | --- |
| `name` | spider 名稱（`scrapy crawl <name>`） |
| `start_urls` / `start_requests()` | 起始請求；需要自訂 header、POST 時才寫 `start_requests()` |
| `parse(response)` | 預設 callback；`response` 同時是 selector（`.css`、`.xpath`）與請求資訊（`.url`、`.status`） |
| `yield response.follow(url, callback=...)` | 排入新請求；Scrapy 會自動去重已抓過的 URL |
| `yield {...}` | 輸出一筆資料，交給 `FEEDS` 寫檔 |

> 正式專案用 `scrapy startproject` 建立目錄結構，設定放 `settings.py`，在終端機跑 `scrapy crawl courses -O courses.jsonl`；`CrawlerProcess` 適合單檔腳本。在 Jupyter 裡第二次 `process.start()` 會報 `ReactorNotRestartable`，需重啟 kernel。

## 選 selector 的流程

1. 在 DevTools 找到重複的容器（卡片、表格列）。
2. 只選一個區塊，抽出一個欄位並確認正確。
3. 推廣到所有區塊；缺欄位用 `.get(default=...)`。
4. 最後才加分頁與跟隨連結。

| 常見錯誤 | 改法 |
| --- | --- |
| 只取直接文字，內容其實在 `<a>` / `<span>` 裡 | `//text()`、`::text` 前加空白，或 `string()` |
| `@class="..."` 完全比對，頁面有多個 class | CSS `.class` 或 XPath `contains(@class, ...)` |
| 在區塊迴圈中寫 `//`，抓到整頁的值 | 改用 `./` 或 `.//` |
| 手動串 URL（`base + href`） | `response.follow()` 或 `urljoin()` |
| 抽到整段 HTML 而不是文字 | 選取最後加 `::text` / `/text()` / `::attr()` |
