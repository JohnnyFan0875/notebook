# Web Scraping in R

在 R 裡做 web scraping，通常是把三件事接起來：

- 用 `xml2` / `rvest` 讀取與解析 HTML。
- 用 CSS selector 或 XPath 找到目標節點。
- 用 `httr` 或其他 HTTP 工具處理請求、headers 和抓取節奏。

重點不只是「抓到資料」，而是分清楚你到底在處理哪一層：

- HTML 結構
- selector 邏輯
- HTTP 請求

## 基本流程

```r
library(rvest)

page <- read_html("https://example.com")

titles <- page %>%
  html_elements("h2") %>%
  html_text2()
```

最常見的 pipeline 是：

1. `read_html()` 取得 HTML 文件
2. `html_element()` 或 `html_elements()` 定位節點
3. `html_text2()`、`html_attr()`、`html_table()` 抽出可用資料

## HTML 的心智模型

HTML 是一棵樹，不是平面文字。真正決定你能不能穩定抓資料的，是你有沒有看懂節點之間的父子與巢狀關係。

例如：

```html
<html>
  <body>
    <div>
      <h2>A first example</h2>
      <p>A text paragraph.</p>
    </div>
  </body>
</html>
```

如果你不知道目標內容是在 `div > p`、`table td.role` 還是某個帶 class 的 `span`，selector 很容易越寫越脆弱。

## `html_element()` 與 `html_elements()`

```r
page %>% html_element("body")
page %>% html_elements("div p")
```

- `html_element()`：取第一個符合條件的節點。
- `html_elements()`：取所有符合條件的節點。

實務上如果頁面有多筆重複卡片、列或表格列，通常要用 `html_elements()`；如果只該有唯一標題或主容器，用 `html_element()` 比較自然。

## 抽文字、屬性與表格

### 文字

```r
page %>%
  html_elements("p") %>%
  html_text2()
```

### 屬性

```r
page %>%
  html_element("a") %>%
  html_attr("href")
```

如果想看全部屬性：

```r
page %>%
  html_element("a") %>%
  html_attrs()
```

### 表格

```r
page %>%
  html_element("table") %>%
  html_table()
```

若表格沒有 `<th>` 欄名，可嘗試：

```r
page %>%
  html_element("table") %>%
  html_table(header = TRUE)
```

`html_table()` 很方便，但也要小心：

- 合併儲存格常讓結果變形。
- 頁面上的表格不一定就是你想像中的 tidy table。
- 抓完後通常還是要做欄名與型別清理。

## CSS Selectors

對大多數 scraping 任務，CSS selector 已經夠用，而且通常比 XPath 更短、更好讀。

### Type selectors

```r
page %>% html_elements("h1")
page %>% html_elements("a, span")
page %>% html_elements("*")
```

### Class 與 ID

```r
page %>% html_elements(".alert")
page %>% html_elements("#special")
page %>% html_elements("div#special")
page %>% html_elements("a.alert")
```

如果節點要同時有兩個 class：

```r
page %>% html_elements(".alert.emph")
```

注意這和 `.alert, .emph` 不一樣：

- `.alert.emph`：同時具有兩個 class 的節點
- `.alert, .emph`：符合任一 selector 的節點

### Descendant 與 child

```r
page %>% html_elements("div p")
page %>% html_elements("div > p")
```

- `div p`：任何在 `div` 裡面的後代 `p`
- `div > p`：只有直接子節點 `p`

很多 selector 抓太多資料，就是因為把這兩者混在一起。

## 什麼時候改用 XPath

當 CSS 很難表達條件時，XPath 會更有力，特別是：

- 要依節點位置選擇
- 要根據子節點條件過濾父節點
- 要寫比較細的 predicate

基本形式：

```r
page %>% html_elements(xpath = "//p")
page %>% html_elements(xpath = "//body//p")
page %>% html_elements(xpath = "/html/body//p")
```

可以先這樣記：

- `//`：從目前範圍往下找任意後代
- `/`：直接往下一層
- `[...]`：加條件

### XPath 範例

```r
page %>% html_elements(xpath = "//div/p")
page %>% html_elements(xpath = "//*[@id = 'special']//div")
page %>% html_elements(xpath = "//span/a[@class = 'external']")
```

有些條件 CSS 很難寫，XPath 很直：

```r
page %>% html_elements(xpath = "//div[a]")
```

意思是「選出包含 `<a>` 子節點的 `div`」。

### `position()` 與進階 predicates

```r
page %>% html_elements(xpath = "//ol/li[position() = 2]")
page %>% html_elements(xpath = "//ol/li[position() < 3]")
page %>% html_elements(xpath = "//ol[count(li) > 2]")
```

這類條件適合：

- 只抓第二個或前幾個元素
- 按子節點數量過濾容器
- 從結構規則而不是 class 名稱來定位

如果頁面結構很規則，XPath 常能比一長串 CSS 更穩。

## 局部抓取比全域抓取穩

比起直接對整頁寫超長 selector，通常更穩的方式是先縮小到區塊，再向下抽欄位。

```r
rows <- page %>% html_elements("#cast tr")

roles <- rows %>%
  html_element("td.role") %>%
  html_text2()
```

這種寫法的好處：

- selector 比較短
- debug 比較容易
- 如果某一列缺欄位，比較容易定位問題

## HTTP 層：不是每個頁面都只靠 `read_html(url)` 就夠

Scraping 背後是 HTTP request / response。至少要知道：

- `GET`：取資料
- `POST`：送資料給伺服器，例如表單提交
- 常見狀態碼：`200`, `404`, `3xx`, `5xx`

用 `httr` 可以先看 response：

```r
library(httr)

response <- GET("https://httpbin.org")
status_code(response)
content(response)
```

這在幾種情況特別重要：

- 你懷疑被 redirect
- 網頁其實沒有成功返回內容
- 伺服器需要特定 headers

## Custom User-Agent

如果你在抓別人的網站，最好明確表明自己是誰，而不是完全沿用預設 UA。

```r
library(httr)

response <- GET(
  "https://example.com",
  user_agent("Research scraper for personal notebook; contact: you@example.com")
)
```

這不只是禮貌，也有助於站方在需要時聯繫你，而不是把流量直接當成匿名可疑請求。

## 控制抓取速度

很多 scraping 問題不是 selector 錯，而是你抓太快。

如果需要批次抓多個頁面，至少加入延遲：

```r
library(httr)
library(purrr)

slow_get <- purrr::slowly(~ GET(.x), rate = rate_delay(3))

urls <- c("https://example.com/a", "https://example.com/b")
responses <- map(urls, slow_get)
```

原則很簡單：

- 不要對同一網站瞬間連發大量請求
- 尊重 robots / 使用條款
- 失敗時重試也要有節制

## 什麼情況 selector 會失效

常見原因：

- class 名稱是動態生成的
- 頁面結構改版
- 你抓到的是 JS 初始骨架，不是真正資料
- 你以為資料在 HTML，其實在 API 回應裡

所以 debug 順序通常是：

1. 先確認 HTTP response 是否成功
2. 再確認原始 HTML 裡是否真的有目標資料
3. 最後才調 selector

如果原始 HTML 沒資料，繼續調 CSS / XPath 通常只是浪費時間。

## 實務選擇

- 簡單頁面、穩定 class、一般節點抓取：先用 CSS selector。
- 需要位置條件、父子條件、進階 predicate：改用 XPath。
- 需要看 status code、headers、user-agent、節流：補上 `httr`。
- 如果頁面資料本質上是表格，先試 `html_table()`，再決定是否手拆節點。

在 R 裡做 scraping，真正重要的不是記住所有 selector，而是先搞清楚資料是在 HTML tree 的哪裡，以及你現在卡在 HTML、selector，還是 HTTP 這一層。
