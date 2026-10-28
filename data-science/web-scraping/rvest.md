[Data Science](../README.md) › [Web Scraping](README.md) › rvest

# rvest：R 的網頁擷取

R 的 scraping 分三層：`httr2` 處理 HTTP 請求（headers、節流、重試），`rvest`（建立在 `xml2` 上）解析 HTML，CSS / XPath selector 定位節點。卡住時先分清楚問題在哪一層。Selector 語法對照與共用原則見 [Web Scraping](README.md#共用觀念)；Python 對應見 [BeautifulSoup 與 Selenium](beautifulsoup-selenium.md)。

## 基本流程

```r
library(rvest)

page <- read_html("https://example.com")       # 1. 取得 HTML 文件

page |>
  html_elements("h2") |>                       # 2. 定位節點（全部）
  html_text2()                                 # 3. 抽出文字
```

| 步驟 | 函式 | 說明 |
| --- | --- | --- |
| 讀取 | `read_html(url 或 檔案 或 字串)` | 靜態 HTML |
| 讀取（動態頁） | `read_html_live(url)` | rvest ≥ 1.0.4；透過 chromote 開真的 Chrome 執行 JS，可 `$click()`、`$scroll_to()` |
| 定位一個 | `html_element(css)` | 每個輸入節點回傳一個結果，找不到為 missing，**長度不變** |
| 定位全部 | `html_elements(css)` | 所有符合的節點，長度可能變 |
| 文字 | `html_text2()` | 模擬瀏覽器顯示：處理 `<br>`、合併空白；`html_text()` 回傳原始文字 |
| 屬性 | `html_attr("href")` / `html_attrs()` | 單一屬性 / 全部屬性 |
| 表格 | `html_table()` | 回傳 tibble；`html_elements("table")` 後得到 tibble 的 list |
| 相對連結 | `url_absolute(href, base)` | 轉成完整網址 |

## 選取與抽值

```r
# CSS selector
page |> html_elements("a, span")               # 任一
page |> html_elements(".alert.emph")           # 同時有兩個 class（與 ".alert, .emph" 不同）
page |> html_elements("div p")                 # 後代
page |> html_elements("div > p")               # 直接子節點

# XPath：依位置、子節點條件、文字
page |> html_elements(xpath = "//ol/li[position() < 3]")
page |> html_elements(xpath = "//ol[count(li) > 2]")
page |> html_elements(xpath = "//div[a]")      # 含 <a> 子節點的 div
page |> html_elements(xpath = "//span/a[@class = 'external']")

# 屬性與表格
page |> html_elements("a") |> html_attr("href") |> url_absolute("https://example.com")
tbl <- page |> html_element("table") |> html_table()   # 第一列 <th> 自動當欄名
```

`html_table()` 的結果仍要清理：合併儲存格會讓列變形、數字欄常帶逗號或註腳符號（`readr::parse_number()`）、欄名可能重複（`janitor::clean_names()`）。

### 局部抓取：先選列，再抓欄位

```r
rows <- page |> html_elements("#cast tr")

cast <- tibble::tibble(
  actor = rows |> html_element("td.actor") |> html_text2(),
  role  = rows |> html_element("td.role")  |> html_text2()   # 某列缺 role → NA，不會錯位
)
```

> 這裡一定要用單數的 `html_element()`：它對每一列各回傳一個結果，缺的補 `NA`，所以兩個欄位長度一致。若用 `html_elements()`，缺值的列會被跳過，欄位長度不同，資料就錯位了。

## HTTP 層：httr2

`read_html(url)` 無法設定 headers、處理錯誤狀態碼或節流。需要這些時，先用 `httr2` 取得回應，再把 body 交給 rvest。

```r
library(httr2)

req <- request("https://example.com/list") |>
  req_user_agent("mylab-scraper/0.1 (me@uni.edu)") |>   # 表明身分
  req_throttle(rate = 20 / 60) |>                        # 每分鐘最多 20 次（同一 realm 共用）
  req_retry(max_tries = 3)                               # 429 / 503 自動退避重試

resp <- req_perform(req)                                 # 4xx / 5xx 會直接拋錯
resp_status(resp)                                        # 200
page <- resp |> resp_body_html()                         # 交給 rvest
page |> html_elements("h2") |> html_text2()

# 批次抓多頁：節流設定跟著 request 走
urls  <- c("https://example.com/a", "https://example.com/b")
pages <- purrr::map(urls, \(u) request(u) |>
                      req_user_agent("mylab-scraper/0.1 (me@uni.edu)") |>
                      req_throttle(rate = 20 / 60) |>
                      req_perform() |>
                      resp_body_html())
```

| 舊寫法（httr） | httr2 |
| --- | --- |
| `GET(url)` | `request(url) \|> req_perform()` |
| `status_code(r)` | `resp_status(resp)` |
| `content(r)` | `resp_body_html()` / `resp_body_json()` / `resp_body_string()` |
| `user_agent("...")` | `req_user_agent("...")` |
| `purrr::slowly(GET, rate_delay(3))` | `req_throttle(rate = 1 / 3)` |
| 手寫重試迴圈 | `req_retry(max_tries = 3)` |

API 請求、認證、分頁的 R 寫法見 [匯入資料（R）](../r-foundations/importing-data.md#http-與-api)。

### polite：遵守 robots.txt 與節流

```r
library(polite)

session <- bow("https://example.com", user_agent = "mylab-scraper/0.1 (me@uni.edu)")  # 讀 robots.txt、設定延遲
page <- session |> nod("/list") |> scrape()      # 被 robots.txt 禁止時回傳 NULL 並警告
```

`polite` 會自動快取並依 robots.txt 的 crawl-delay 節流，適合在不熟悉的網站上先用。

## 什麼時候 selector 會失效

| 原因 | 判斷 | 對策 |
| --- | --- | --- |
| 資料由 JavaScript 產生 | `read_html()` 結果裡搜不到目標文字 | 找 Network 裡的 JSON 端點；不行再 `read_html_live()` |
| class 名稱動態產生 | 類似 `css-1x2y3z`、每次改版都變 | 改用 `id`、`data-*` 或結構（XPath 位置、子節點條件） |
| 頁面改版 | 昨天能跑今天全是 `NA` | selector 集中放一處，抓完檢查 `NA` 比例 |
| 請求失敗或被導向 | `resp_status()` 不是 200、內容是登入頁 | 先檢查 HTTP 層 |

除錯順序：HTTP 回應是否成功 → 原始 HTML 是否真的有資料 → 最後才調 selector。
