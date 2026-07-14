# Web Scraping

這個章節整理如何從網頁收集資料。重點不只是抓到內容，更包括如何判斷網站結構、選擇適合的工具，以及避免把一次性腳本寫成脆弱且難維護的流程。

## 建議閱讀順序

1. 先確認是否真的需要 scraping：若網站已有 API，通常應優先讀 [API HTTP](../python-foundations/api-http.md) 或相關資料擷取說明，而不是直接抓 HTML。
2. 再讀 [BeautifulSoup and Selenium](beautifulsoup-selenium.md)，理解靜態頁面、動態頁面、登入流程與等待機制的差異。
3. 若要把抓回來的資料接到清理與分析，回頭搭配 [Data Manipulation and EDA](../data-manipulation-and-eda/README.md) 與 [Data Engineering](../data-engineering/README.md)。

## Topics

- [BeautifulSoup and Selenium](beautifulsoup-selenium.md)

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
- [R Foundations](../r-foundations/README.md): 如果主要工作流在 R，可對照 [Web Scraping in R](../r-foundations/web-scraping-in-r.md)。
- [Data Engineering](../data-engineering/README.md): 當 scraping 不再是一次性行為，而是資料管線的一部分時，要回到 ingestion、governance 與可重跑設計。
- [Data Manipulation and EDA](../data-manipulation-and-eda/README.md): 抓到資料後，真正的工作通常才開始。

## 實務提醒

- scraping 成功不代表資料可用，還要檢查欄位型別、重複值、時間戳與缺值模式。
- 若網站結構常變，應先把 selector、等待條件與錯誤處理抽成可維護的模組，而不是散落在 notebook。
- 來源條款、robots 規範與請求頻率控制屬於工作流程的一部分，不是事後補充。
