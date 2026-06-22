# ETL

## ETL as a Practical Workflow

ETL 不是抽象縮寫而已，而是一種把資料需求變成可重跑流程的方式：

1. Extract
2. Transform
3. Load

它的重點不是每一步都很複雜，而是每一步都要能被明確描述、重現與自動化。

## ETL and ELT

ETL 與 ELT 都是在搬資料，但轉換發生的位置不同。

| Pattern | Flow | 常見場景 |
| --- | --- | --- |
| ETL | extract -> transform -> load | 先在外部程式整理資料，再載入目標系統 |
| ELT | extract -> load -> transform | 先把資料載入 warehouse 或 lakehouse，再利用平台算力轉換 |

實務上可以這樣理解：

- ETL 比較像先把資料洗乾淨，再交給下游。
- ELT 比較像先把資料送進分析平台，再在平台內部整理。
- ETL 常同時處理 tabular 與 non-tabular sources。
- ELT 則更常出現在以 warehouse 為核心、資料格式較偏 tabular 的分析環境。

## From Business Need to ETL

很多 ETL 專案其實都從一個很簡單的需求開始，例如：

- 取得 rating data
- 清理並算出 top recommended items
- 每天重新計算
- 提供給 dashboard 或應用程式

這類需求之所以屬於 data engineering，是因為它不只是一次分析，而是要穩定地每天重做，並讓下游可以持續依賴結果。

## The Three Stages

### Extract

從來源系統取出資料。

來源可能是：

- 資料庫 tables
- flat files
- API responses
- web data

### Transform

把原始資料轉成下游可用的形式。

常見工作包括：

- 清理錯誤值
- 合併多個來源
- 補欄位與計算指標
- 建立推薦、彙總或特徵表

如果來源含有 JSON、API responses 或其他半結構化資料，transform 往往還包含：

- parsing nested fields
- 補上 metadata
- 把非表格格式整理成穩定 schema

### Load

把結果寫入目標系統，供下游使用。

常見目標包括：

- analytics tables
- dashboard backend
- feature store 或模型輸入表

常見做法是把整理後的 DataFrame 寫入 SQL table、warehouse table 或其他可查詢儲存層。重點不只是寫成功，而是讓下游可以穩定取得同樣結構的資料。

在 Python workflow 裡，load 階段也常會明確決定：

- 寫入哪個 table 或 destination
- `append`、`replace` 或 upsert 的策略
- 是否保留 index、主鍵或時間欄位

## ETL vs. One-Off Analysis

一次性分析比較常問：

- 這次能不能算出答案？

ETL 比較常問：

- 這個流程明天還能不能穩定再跑一次？
- 如果來源延遲或格式改了，怎麼辦？
- 下游是不是能持續拿到一致結果？

## Practical Reminders

- 一個 ETL workflow 的價值，在於穩定重跑，不在於第一次成功。
- 轉換步驟最好能明確區分 raw data 與 curated output，避免覆蓋原始資料。
- 如果結果要每日更新、服務 dashboard 或產品功能，它通常就已經不是單純分析腳本，而是 pipeline。

[Back to Data Engineering](README.md)
