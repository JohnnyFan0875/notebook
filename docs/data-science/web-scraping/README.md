# Web Scraping

這個章節整理如何從網頁收集資料。重點不只是抓到內容，更包括如何判斷網站結構、選擇適合的工具，以及避免把一次性腳本寫成脆弱且難維護的流程。

## Topics

- [BeautifulSoup and Selenium](beautifulsoup-selenium.md)

## 工具選擇

- 靜態 HTML 頁面：優先用 `requests` + BeautifulSoup。
- 需要登入、點擊、等待 JavaScript 載入：再考慮 Selenium。
- 若網站已有 API，通常優先使用 API，而不是 scraping。
