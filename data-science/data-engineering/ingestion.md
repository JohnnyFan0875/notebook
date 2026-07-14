# Ingestion

## What Ingestion Means

Ingestion 是把資料從來源系統帶進資料平台的第一步。這一步不只是「下載檔案」，而是要先判斷資料來自哪裡、長什麼樣、以及後續是否容易被轉換與追蹤。

## Common Source Shapes

### Flat Files

像 `csv`、`tsv` 這種 flat files 仍然非常常見。

- row 通常代表一筆 record
- column 代表欄位或 attribute
- 優點是簡單、易交換
- 缺點是 schema 約束通常較弱，欄位品質很容易漂移

實務上最常見的讀取入口是 `read_csv()`，但重點不只是把檔案打開，而是先確認：

- delimiter 是不是逗號、tab，或其他分隔符號
- 是否需要 `skiprows` 跳過 metadata header
- 是否應該用 `usecols`、`nrows` 先縮小載入範圍
- 某些欄位是否要先指定 dtype，避免型別推論失真

### Spreadsheets

Excel 或其他 spreadsheet 檔案，本質上也是 tabular data，但通常比 flat files 多了格式、公式與多工作表結構。

- 一個 workbook 可以包含多個 sheets
- 不同 sheet 之間可能代表不同年度、部門或資料切片
- 實務上常需要指定 `sheet_name`、`usecols`、`skiprows`
- 如果多個 sheets 結構一致，可以先分別載入，再補來源欄位後合併

### Plain Text

純文字資料常屬於 unstructured data。

- 人類可讀
- 機器處理前通常需要 parsing
- 若要做下游分析，常要先補 metadata 或轉成更規則的格式

### JSON

JSON 是很常見的 semi-structured ingestion 格式。

- 可以同時包含 atomic values 與 nested objects
- 適合 API 回應與事件資料
- 彈性高，但欄位結構可能隨版本演進而改變
- records 不一定擁有完全相同的 attributes

如果用 pandas 讀 JSON，除了路徑本身，也常要先確認：

- 資料 layout 是否需要指定 `orient`
- 某些欄位是否應該預先指定 dtype
- nested objects 要在 ingestion 階段展平，還是先原樣落地再轉換

### Parquet

Parquet 是常見的 column-oriented file format。

- 適合大量表格資料的儲存與讀取
- 比起純文字格式，通常更節省空間
- 在 analytical workflow 中很常作為中繼層或交換格式
- 與 CSV 一樣都能承載表格資料，但 Parquet 更偏向效能與 schema-aware workflow

### SQL Databases

很多 ingestion 流程不是從檔案開始，而是直接從資料庫查詢。

- 常透過 connection URI 建立連線
- 再以 query 或 table 方式取回資料
- 適合抽取已經有明確 schema 的 transactional 或 operational data
- relational databases 也更容易支援資料型別、鍵值關聯與多使用者並行存取

像 SQLite 這類資料庫甚至可以直接是一個檔案；而其他系統則通常需要 engine、帳密與 network access。對 ingestion 來說，差別不在 pandas 語法，而在連線與權限設定。

## Data on the Web

很多資料不是直接放在檔案裡，而是來自 web services。

典型流程是：

1. client 發出 request
2. server 回傳 response
3. response 內容可能是 HTML、JSON、檔案或其他格式

這也是為什麼 data ingestion 常和 API、認證、rate limits、response parsing 綁在一起。

API 往往是資料來源上方的一層介面，而不是直接讓你碰到底層資料庫。這種設計能降低耦合，但也代表 ingestion 必須配合 API 的格式、欄位命名與存取限制。

## What To Decide Early

在設計 ingestion 時，先回答這些問題通常很有幫助：

- 來源是檔案、資料庫、API，還是 event stream？
- 資料是 structured、semi-structured，還是 unstructured？
- 是一次性匯入，還是持續更新？
- 後面要進分析、報表、模型，還是只是先落地保存？
- 日期欄位要在讀取時解析，還是讀進來後再用明確規則轉型？

## Managed Ingestion Workflows

當資料平台走向雲端或整合式產品時，ingestion 不一定是自己寫一支 script，也可能是平台內建的 orchestration 與 transformation 元件。

像 Microsoft Fabric 這類平台，常見會把 ingestion 工作拆成：

- Data Pipelines: 負責 orchestration、排程與多步驟流程
- Dataflows Gen2: 負責 low-code 的資料轉換與載入
- Shortcuts: 用連結方式把既有資料帶進統一資料層，而不是重複複製

這種做法的好處是：ingestion、transformation 與 destination 管理更容易被統一治理。

### Dataflows Gen2 as an Ingestion Tool

Dataflows Gen2 可以把它理解成一個偏 transformation-first 的 ingestion 介面。

常見特徵包括：

- 用 Power Query Online 做圖形化轉換
- 支援大量 transformation，例如 merge、pivot、型別整理
- 能和 Data Pipelines 串接
- 對大資料量提供 staging 與 fast copy 思路

如果團隊想減少手刻程式、又需要規則化的資料整理流程，這類工具會很實用。

### Refresh and Staging

managed ingestion workflow 的重點不只是第一次載入，而是後續 refresh。

像 Dataflows Gen2 這類工具，通常會有：

- refresh 機制，讓 destination 保持最新
- staging 區，暫存轉換過程中的中介結果

中介 staging 常由平台自動管理，不一定給使用者直接操作。這提醒我們一件事：在 managed platform 裡，資料生命週期的一部分已經交給平台接管，所以要更清楚知道哪一層是 raw、哪一層是 temporary、哪一層是 serving。

## Practical Reminders

- ingestion 的第一個錯誤，往往不是程式讀不到資料，而是把資料型態判錯。
- JSON 很方便，但 nested schema 若不先規劃展開方式，後面會很痛苦。
- landing 階段先保留原始資料通常是好習慣，因為你未來很可能需要重跑轉換。
- 如果來源是 SQL 或 API，先把 connection、query 與認證邏輯模組化，後面會比較容易維護與測試。
- `parse_dates` 這類自動解析很好用，但如果來源日期格式不標準，通常要在載入後用明確規則轉換，不要盲信自動推論。
- 如果使用平台內建 ingestion 工具，也要先分清楚 orchestration、transformation、shortcut linking 與 destination 載入各自屬於哪一層。

[Back to Data Engineering](README.md)
