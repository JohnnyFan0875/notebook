[Data Science](../README.md) › Web Scraping

# 網頁擷取 (Web Scraping)

從 HTML 網頁抽出結構化資料。抓到內容只是第一步，真正的工作在於判斷資料在哪一層（HTML、JavaScript 還是背後的 API）、寫出改版也不易壞的 selector，並守住請求頻率與使用條款。

## 先決定要不要 scraping

```
有官方 API / 下載檔？ ──是──→ 用 API（見 API 與 HTTP），不要抓 HTML
        │否
DevTools → Network 看得到 XHR / fetch 回傳的 JSON？ ──是──→ 直接呼叫那個 JSON 端點
        │否
「檢視原始碼」裡有目標資料？ ──是──→ 靜態頁：requests + BeautifulSoup / parsel，R 用 rvest
        │否（資料由 JavaScript 產生、需要登入或點擊）
動態頁：Selenium / Playwright；R 用 rvest::read_html_live()
```

> 生資常見資料來源幾乎都有 API 或批次下載：NCBI E-utilities、Ensembl REST、UniProt REST、GEO / SRA 的 FTP。先查文件再考慮 scraping，用法見 [API 與 HTTP](../python-foundations/api-http.md)。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [BeautifulSoup 與 Selenium](beautifulsoup-selenium.md) | `requests` + BeautifulSoup 解析靜態頁；Selenium 4 操作動態頁、等待、headless | 靜態頁怎麼抓？要點擊或等 JS 載入怎麼辦？ |
| [Scrapy 與 Selector](scrapy-and-selectors.md) | CSS / XPath 抽文字與屬性、`.get()` / `.getall()`、spider 跟隨連結、輸出與節流設定 | 怎麼精準選到元素？多頁爬取怎麼組織？ |
| [rvest（R）](rvest.md) | `read_html` → `html_elements` → `html_text2` / `html_table`；httr2 請求與節流、`polite` | 在 R 裡怎麼做同樣的事？ |

## 共用觀念

三篇工具筆記共用以下觀念，各篇只講工具用法。

### HTML 是一棵樹

```html
<html>
  <body>
    <div id="content" class="course-block">
      <a href="/course/python">Python Course</a>
      <p>Hello world</p>
    </div>
  </body>
</html>
```

| 概念 | 說明 |
| --- | --- |
| tag / attribute | tag 定義結構，attribute 加上 metadata（`id`、`class`、`href`、`data-*`） |
| `id` / `class` | `id` 理應唯一；`class` 可重複，一個元素可有多個 class（`class="a b"`） |
| 文字位置 | 常藏在巢狀子節點裡（`<p>Hello <a>world</a></p>`），不在第一眼看到的元素上 |
| 局部抓取 | 先選重複的區塊（卡片、表格列），再在區塊內找欄位；比對整頁寫一條長 selector 穩，缺欄位時也容易定位 |

先在瀏覽器 DevTools（Elements 面板）看懂父子關係，右鍵 → Copy selector 只當起點，產生的路徑通常太長太脆弱。

### CSS selector vs XPath

| 目的 | CSS selector | XPath |
| --- | --- | --- |
| 依標籤 | `p` | `//p` |
| 依 class / id | `.alert`、`#uid`、`div#uid` | `//*[@class="alert"]`、`//*[@id="uid"]` |
| class 含某個 token | `.alert`（自動處理多 class） | `//*[contains(@class, "alert")]` |
| 同時有兩個 class | `.alert.emph` | `//*[contains(@class,"alert") and contains(@class,"emph")]` |
| 後代 / 直接子節點 | `div p` / `div > p` | `//div//p` / `//div/p` |
| 第 n 個 | `li:nth-of-type(2)` | `//li[2]`、`//li[position() < 3]` |
| 屬性值 | `a::attr(href)`（parsel） | `//a/@href` |
| 依文字內容 | 無標準寫法 | `//p[contains(text(), "Hello")]` |
| 依子節點條件選父節點 | `div:has(> a)`（CSS4，支援度不一） | `//div[a]`、`//ol[count(li) > 2]` |
| 往上找父節點 | 無 | `..`、`ancestor::div` |

哪個讓 selector 最好讀就用哪個；需要依文字、往上找父節點或計數條件時改用 XPath。

### 禮貌與合法性

| 項目 | 做法 |
| --- | --- |
| 先找 API | 有官方 API 或下載檔就不要抓 HTML |
| robots.txt / 使用條款 | 抓取前確認；Python 可用 `urllib.robotparser`，R 用 `polite::bow()` |
| User-Agent | 表明身分與聯絡方式（`mylab-scraper/0.1 (me@uni.edu)`），不要偽裝成瀏覽器或輪換 UA 規避封鎖 |
| 節流 | 每次請求間隔至少 1 秒；Python `time.sleep(random.uniform(1, 3))`、Scrapy `DOWNLOAD_DELAY`、R `req_throttle()` |
| 重試 | 只對 429 / 5xx 重試，指數退避並設上限；遵守 `Retry-After`（見 [API 與 HTTP](../python-foundations/api-http.md#session重試與限速)） |
| 快取 | 原始 HTML 存檔再解析：selector 寫錯時不必重抓，也讓結果可重現 |
| 個資與版權 | 含個人資料的內容受隱私法規約束（見 [Responsible AI](../responsible-ai/README.md)）；抓得到不等於可以再散布 |

### 常見失敗與除錯順序

| 症狀 | 常見原因 | 檢查 |
| --- | --- | --- |
| 回傳空結果 | 資料由 JavaScript 載入；HTML 只有骨架 | 「檢視原始碼」搜尋目標文字；找 Network 裡的 JSON |
| 403 / 429 | 沒有 UA、請求太快、被判定為機器人 | 狀態碼、`Retry-After`；放慢速度 |
| 文字缺一截 | 只取了直接文字節點，內容在子標籤裡 | 改用後代文字（`//text()`、`::text` 前加空白、`get_text()`） |
| 昨天能跑今天壞 | 網站改版、class 名稱是動態產生的（`css-1x2y3z`） | 改用穩定屬性（`id`、`data-*`、語意結構） |
| 欄位錯位 | 某些區塊缺欄位，全域抓取把不同列的值串在一起 | 改成先選區塊再抓欄位，缺值補 `None` / `NA` |

除錯順序：HTTP 狀態碼 → 原始 HTML 裡是否真的有資料 → 最後才調 selector。原始 HTML 沒有資料時，調 selector 只是浪費時間。

## 抓完之後

- 抓到的都是字串：數字、日期要轉型，並檢查重複列、缺值、單位與編碼（見 [資料處理與 EDA](../data-manipulation-and-eda/README.md)）。
- 要定期重跑時，把 selector、等待條件、錯誤處理抽成模組，記錄抓取時間與來源 URL，並把它當成資料管線的一環（見 [Data Engineering](../data-engineering/README.md)）。
