# Storage and Models

## Three Common Data Shapes

### Structured Data

Structured data 有固定欄位、明確型別，通常能用 rows and columns 表示。

常見特徵：

- 容易搜尋與組織
- 型別明確
- 可以透過關聯形成 schema
- 常放在 relational databases
- 通常以 SQL 建立與查詢

### Semi-Structured Data

Semi-structured data 有一定結構，但不要求每筆資料都完全同型。

常見特徵：

- 比完全非結構化資料更容易搜尋
- 結構比較鬆
- 不同觀測可能欄位數不同
- 常見格式有 JSON、XML、YAML

### Unstructured Data

Unstructured data 不適合直接塞進表格欄列模型，例如文字、圖片、聲音、影片。

常見特徵：

- 難以直接搜尋與整理
- 常需要額外 metadata 或 embedding 才能有效使用
- 常存放在 data lakes，也可能出現在 warehouse 或 database 的某些欄位中

## Adding Structure Back

很多高價值資料其實一開始是非結構化的。實務上常見做法是先補 metadata，或用 AI/ML 幫忙抽出可索引資訊，把 unstructured data 逐步轉成 semi-structured。

## Databases, Warehouses, and Lakes

在現代資料架構裡，storage 不只是一個資料庫選型問題，而是要根據資料型態與消費方式，把資料放到最合適的系統。

### Database

Database 是最廣義的概念，指有組織地儲存並可被存取的資料集合。

- data warehouse 是一種 database
- database 不一定是 data warehouse

### Data Warehouse

Data warehouse 偏向分析用途。

常見特徵：

- 儲存特定用途的資料
- 以 structured data 為主
- 更新成本通常較高
- 查詢與分析效率較好

在整合式平台裡，warehouse 往往也更直接連到 semantic layer、BI 報表與 SQL-first analytics workflow。

### Data Lake

Data lake 偏向保留原始資料與多樣型態資料。

常見特徵：

- 保留大量 raw data
- 可容納多種資料結構
- 容量通常更大、成本相對更低
- 彈性高，但直接分析難度也更高

在像 Microsoft Fabric 這類平台裡，lakehouse 常扮演把 data lake 的彈性和 table-style 分析入口結合起來的角色。

### Blob Storage

Blob storage 專門處理大型物件與非結構化資料，常被用來當作 data lake 的底層儲存之一。

常見特徵：

- 支援多種資料型態，包含非結構化資料
- 幾乎可視為無上限擴充
- 單位成本通常較低

常見用途：

- media storage
- backup and archiving
- landing zone
- content delivery

## Delta Lake as a Lakehouse Table Layer

在 lakehouse 場景裡，單純把 Parquet 檔放進 storage 還不一定夠。很多平台會再加上一層 table-aware storage abstraction，讓檔案更像可維護的資料表。

Delta Lake 就是這種 storage layer 的典型例子。

它的重要特徵包括：

- 建立在 Parquet 之上
- 提供 ACID transactions
- 保留 metadata 與 table versioning 能力
- 讓多個工具可以圍繞同一份 table format 協作

在 Microsoft Fabric 這類平台裡，Delta Lake table format 常被當成 lakehouse 的標準表格式，這也是為什麼 notebook、SQL endpoint 與其他體驗比較容易互通。

## Unified Storage Layers in Managed Platforms

現代平台常會把底層儲存再包成更統一的體驗。

例如 Microsoft Fabric 的 `OneLake`，就可以被理解成整個 tenant 共用的 unified storage layer。這種設計的重點不是創造一種全新資料型態，而是讓 lakehouse、warehouse、pipelines、dataflows 等元件可以圍繞同一個資料底座運作。

從資料工程角度看，這代表：

- storage 跟 compute、semantic layer 的耦合更緊
- 權限與路徑設計會直接影響多工具協作
- ingestion 可以更容易接上 reporting 與 BI 消費層

## Data Lake vs. Data Warehouse

| 面向 | Data Lake | Data Warehouse |
| --- | --- | --- |
| 資料內容 | 原始資料為主 | 特定用途資料為主 |
| 結構 | 可容納各種結構 | 主要是 structured data |
| 分析便利性 | 較低 | 較高 |
| 成本與彈性 | 較具成本彈性 | 更新與維護通常較昂貴 |

## Shortcuts and Logical Linking

有些平台支援 shortcuts，也就是用邏輯連結方式把資料帶進統一存取層，而不是再複製一次。

這種設計的好處包括：

- 減少重複搬運資料
- 保留既有來源位置
- 讓不同工作區或儲存位置被統一掛接

但也會帶來新的治理問題：

- shortcut path 和 target path 權限要分開思考
- 刪除 shortcut 不代表刪除目標資料
- 讀寫能力可能取決於 shortcut 與 target 兩端的 permission 組合

所以 shortcuts 很方便，但本質上是在 storage 與 access layer 之間增加一層邏輯映射。

## Why Catalogs Matter

不論是 lake、warehouse 或一般 database，只要資料規模變大，就需要 data catalog 幫團隊回答這些問題：

- 這份資料從哪裡來？
- 誰在使用它？
- 欄位代表什麼？
- 更新頻率與品質狀態如何？

沒有 catalog，資料不是真的「不可用」，但會很快變成只有少數人看得懂的黑盒子。

## SQL in Context

SQL 對 data engineering 很重要，但角色跟 data science 稍有不同：

- data engineers 常用 SQL 建立、維護、更新 tables 與 schema
- data scientists 常用 SQL 查詢、過濾、分組與聚合資料

## SQL vs. NoSQL in Practice

### SQL Databases

- 適合 transactional applications、複雜查詢、以及強調 consistency and integrity 的情境
- 以 structured data 為主

### NoSQL Databases

- 適合高擴充需求、高吞吐情境，或可以接受 eventual consistency 的場景
- 常見於 semi-structured data、key-value、document、graph、time-series 類型資料

不要把 NoSQL 理解成「SQL 的升級版」。它通常是在資料模型或延遲需求不適合傳統 relational design 時的替代方案。

## Databases vs. File Storage

- databases 通常更有組織，也提供搜尋、查詢、replication 等附加能力
- file storage 通常更簡單、更鬆散，但在 raw landing 與大檔案保存上很常見

如果你需要強 schema、查詢能力與資料一致性，database 往往更適合；如果你只是先把原始檔安全放進系統，file storage 往往更自然。

## Practical Reminders

- 不要把 data lake 想成 warehouse 的便宜版，它們解決的是不同問題。
- 選 storage 時先問：這份資料更像 raw landing zone，還是已經是服務分析的整理結果？
- schema 設計與 catalog 品質，會直接影響後續查詢效率與協作成本。
- 統一儲存層不會自動解決治理問題，反而更需要把 lakehouse、warehouse、shortcut 與權限邊界講清楚。
- 在 lakehouse 裡，table format 不是小細節；像 Delta Lake 這種 storage layer 會直接影響交易一致性、維護方式與跨工具互通性。

[Back to Data Engineering](README.md)
