[Computing](../README.md) › Web 開發

# Web 開發 (Web Development)

從瀏覽器與 HTTP 的運作，到用 Python 寫 API、用 React 寫前端。對資料工作者最常見的需求是：把模型或資料包成 API、做一個內部用的查詢介面或 dashboard。

```
Web 基礎（瀏覽器、HTTP、REST）──┬─► FastAPI（伺服器端 API）
                                 └─► React（前端 UI）
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Web 基礎](web-fundamentals.md) | 頁面載入流程、HTML / CSS / JS 分工、HTTP、REST、CORS、開發者工具 | 輸入網址到看到頁面發生了什麼？ |
| [FastAPI](fastapi.md) | 端點、Pydantic 驗證、CRUD 與狀態碼、`TestClient` 測試、部署 | 怎麼用 Python 把資料或模型包成 API？ |
| [React](react/README.md) | 元件、Hooks、CSR / SSR / SSG | 怎麼做互動式前端？ |

| 相關 | 位置 |
| --- | --- |
| 用 Python 呼叫 API（客戶端） | [API 與 HTTP](../../data-science/python-foundations/api-http.md) |
| 從網頁抓資料 | [網頁爬蟲](../../data-science/web-scraping/README.md) |
| 容器化部署 | [Docker](../containers-and-env/docker/README.md) |
| 模型服務與監控 | [部署與監控](../../data-science/machine-learning/production/deployment-and-monitoring.md) |
