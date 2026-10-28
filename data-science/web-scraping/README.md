# Web Scraping

這個章節整理如何從網頁收集資料。重點不只是抓到內容，更包括如何判斷網站結構、選擇適合的工具，以及避免把一次性腳本寫成脆弱且難維護的流程。

## 建議閱讀順序

1. 先確認是否真的需要 scraping：若網站已有 API，通常應優先讀 [API HTTP](../python-foundations/api-http.md) 或相關資料擷取說明，而不是直接抓 HTML。
2. 讀 [Scrapy and Selectors](scrapy-and-selectors.md)，掌握 CSS / XPath selector 與從 HTML 抽出欄位的基本功。
3. 再讀 [BeautifulSoup and Selenium](beautifulsoup-selenium.md)，理解靜態頁面、動態頁面、登入流程與等待機制的差異。
4. 主要用 R 的話，讀 [rvest](rvest.md)。
5. 若要把抓回來的資料接到清理與分析，回頭搭配 [Data Manipulation and EDA](../data-manipulation-and-eda/README.md) 與 [Data Engineering](../data-engineering/README.md)。

## Topics

- [Scrapy and Selectors](scrapy-and-selectors.md)
- [BeautifulSoup and Selenium](beautifulsoup-selenium.md)
- [Web Scraping in R (rvest)](rvest.md)

## 共用觀念

三篇工具筆記（Scrapy、BeautifulSoup / Selenium、rvest）共用以下觀念，各篇只講工具用法。

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

- tag 定義結構，attribute 加上 metadata；文字常藏在巢狀子節點裡，不在你第一眼看到的元素上。
- `id` 理應唯一、`class` 可重複出現、`href` 是 `<a>` 的連結目標。
- 先在瀏覽器 DevTools 看懂父子關係（`div > p`、`table td.role`），selector 才不會越寫越脆弱；局部抓取（先選區塊再往下找）比全域抓取穩。

### CSS selector vs XPath

| | CSS selector | XPath |
| --- | --- | --- |
| 適合 | class / id / 子節點等常見選取 | 依位置、文字內容、子節點條件過濾父節點 |
| 例 | `div.course-block > a` | `//div[@id='content']/a[1]`、`//p[contains(text(), 'Hello')]` |
| 語法重點 | `.class`、`#id`、`a b`（後代）、`a > b`（子） | `//` 任意後代、`/` 下一層、`[...]` 條件、`@attr` 屬性 |

哪個讓 selector 最好讀就用哪個，不需要堅持單一風格。

### 禮貌與合法性

| 項目 | 做法 |
| --- | --- |
| 先找 API | 有官方 API 就不要抓 HTML（見 [API HTTP](../python-foundations/api-http.md)） |
| robots.txt / 使用條款 | 抓取前先確認；條款與請求頻率控制是流程的一部分，不是事後補充 |
| User-Agent | 明確表明身分與聯絡方式，不要沿用預設 UA |
| 節流 | 請求間加延遲（Python `time.sleep(random.uniform(1, 3))`、R `purrr::slowly()`）；失敗重試也要有上限 |
| 個資 | 抓到含個人資料的內容時，儲存與使用受隱私法規約束（見 [Responsible AI](../responsible-ai/README.md)） |

## 這一章要解決什麼

- 我怎麼判斷網站是靜態 HTML、動態 JavaScript 頁面，還是其實已經有 API？
- 什麼時候只需要 `requests` + BeautifulSoup，什麼時候才需要 Selenium？
- 如果 scraping 腳本要重跑、排程或交給別人維護，哪些步驟該先結構化？

## 工具選擇

- 靜態 HTML 頁面：優先用 `requests` + BeautifulSoup。
- 需要登入、點擊、等待 JavaScript 載入：再考慮 Selenium。
- 若網站已有 API，通常優先使用 API，而不是 scraping。

## 與其他章節的關係

- [Python Foundations](../python-foundations/README.md): 放程式語法、HTTP、例外處理與腳本結構。
- [R Foundations](../r-foundations/README.md): R 的語法與資料結構；scraping 本身見 [rvest](rvest.md)。
- [Data Engineering](../data-engineering/README.md): 當 scraping 不再是一次性行為，而是資料管線的一部分時，要回到 ingestion、governance 與可重跑設計。
- [Data Manipulation and EDA](../data-manipulation-and-eda/README.md): 抓到資料後，真正的工作通常才開始。

## 實務提醒

- scraping 成功不代表資料可用，還要檢查欄位型別、重複值、時間戳與缺值模式。
- 若網站結構常變，應先把 selector、等待條件與錯誤處理抽成可維護的模組，而不是散落在 notebook。
