[Data Science](../README.md) › [Data Engineering](README.md) › 儲存與資料模型

# 儲存與資料模型 (Storage and Data Models)

儲存選型要看資料的結構化程度與下游怎麼用：原始檔先安全落地、整理好的表給分析查詢、大型陣列用適合切片的格式。本篇整理資料形狀、各種儲存系統與常見檔案格式。

## 三種資料形狀

| 形狀 | 特徵 | 常見格式 / 系統 | 生資例子 |
| --- | --- | --- | --- |
| 結構化 (structured) | 固定欄位與型別，可用 rows × columns 表示 | 關聯式資料庫、CSV、Parquet | 樣本 metadata、計數矩陣、臨床檢驗值 |
| 半結構化 (semi-structured) | 有結構但每筆欄位可不同、可巢狀 | JSON、XML、YAML | API 回應（NCBI E-utilities、Ensembl REST）、FHIR 病歷 |
| 非結構化 (unstructured) | 不適合直接放進表格 | 文字、影像、音訊、影片 | 病理切片、顯微影像、自由文字病歷 |

非結構化資料常靠補 metadata 或用模型抽取資訊（NER、embedding）變成半結構化，才能被索引與查詢。

## 儲存系統

| 系統 | 用途 | 特徵 | 適合 |
| --- | --- | --- | --- |
| 資料庫 (database) | 最廣義：有組織、可存取的資料集合 | 交易、索引、權限、一致性 | 應用程式、多人寫入（OLTP） |
| 資料倉儲 (data warehouse) | 分析與報表 | 結構化、整合過、欄式、查詢快；更新成本較高 | 固定的分析問題、BI |
| 資料湖 (data lake) | 保留大量原始、多樣資料 | 便宜、彈性高；直接分析較難 | raw landing、日後重新處理 |
| Lakehouse | 在 data lake 上加 table 語意與治理 | 開放檔案格式 + 交易 + SQL | 同一份資料同時給工程、分析、ML |
| 物件 / blob 儲存 | 大型物件與檔案 | 幾乎無上限、單價低；S3、GCS、Azure Blob | 定序原始檔、影像、備份、lake 的底層 |

> data warehouse 是一種 database，但 database 不一定是 warehouse；data lake 也不是便宜版的 warehouse，兩者解決不同問題。

| 面向 | Data Lake | Data Warehouse |
| --- | --- | --- |
| 資料內容 | 原始資料為主 | 特定用途、整理過的資料 |
| 結構 | 各種結構 | 主要是結構化 |
| Schema | schema-on-read（讀時才解釋） | schema-on-write（寫入時就檢查） |
| 分析便利性 | 較低 | 較高 |
| 成本 | 儲存便宜、彈性高 | 更新與維護較貴 |

## Lakehouse 的 table 層：Delta Lake 等

只把 Parquet 檔丟進物件儲存，缺少「表」該有的能力：同時寫入不會互相覆蓋、能回看舊版本、能安全地更新與刪除。table format 在 Parquet 之上加一層 transaction log 補上這些能力。

| Table format | 主要生態 | 特徵 |
| --- | --- | --- |
| Delta Lake | Databricks、Spark | ACID、time travel、`MERGE`；見 [Databricks](databricks.md) |
| Apache Iceberg | Snowflake、AWS、Trino 等多引擎 | 隱藏分區、schema 演進、跨引擎互通 |
| Apache Hudi | Spark、Flink | 偏增量更新與 upsert |

整合式平台（如 Microsoft Fabric 的 OneLake）會把 lakehouse、warehouse、pipeline 圍繞同一個儲存層；要注意的是權限與路徑設計會直接影響多個工具，統一儲存層不會自動解決治理問題。

### Shortcut / 外部連結

有些平台用 shortcut（或 external table、external location）把資料以邏輯連結掛進來，不必再複製一份。

| 好處 | 要注意 |
| --- | --- |
| 減少重複搬運，保留原始位置 | shortcut 與目標兩端的權限要分開檢查 |
| 不同工作區可統一存取 | 刪除 shortcut 不等於刪除目標資料 |

## 檔案格式

| 格式 | 類型 | 優點 | 缺點 | 何時用 |
| --- | --- | --- | --- | --- |
| CSV / TSV | 列式文字 | 人可讀、到處都能開 | 無型別、大、解析慢、Excel 會改基因名 | 小表交換 |
| Parquet | 欄式、壓縮、有 schema | 只讀需要的欄、型別保留、Spark / DuckDB / pandas 原生支援 | 不適合頻繁單筆更新 | 大表分析的預設選擇 |
| Arrow / Feather | 記憶體欄式格式 | 跨語言零複製、讀寫極快 | 不適合長期封存 | Python ↔ R 交換中間結果 |
| HDF5 / AnnData (`.h5ad`) | 階層式陣列容器 | 大型矩陣切片、單細胞標準格式 | 並行寫入困難 | 表現量矩陣 + metadata |
| Zarr | 分塊陣列，適合物件儲存 | 雲端平行讀取、分塊壓縮 | 生態較新 | 雲端上的大型陣列、影像 |
| VCF / BCF | 基因型文字 / 二進位 | 領域標準、可用 tabix 索引 | 寬、查詢慢 | 變異交換；大量分析轉 Parquet / Hail MatrixTable |
| BAM / CRAM | 比對結果二進位 | 可索引隨機存取；CRAM 以參考序列壓縮 | 需要對應的參考基因體版本 | 定序比對結果 |

Parquet 與 HDF5 的 pandas 讀寫見 [記憶體與儲存格式](../python-foundations/pandas/memory-and-storage.md#儲存格式)；用 SQL 直接查 Parquet 見 [DuckDB 與 Parquet](../databases/duckdb-and-parquet.md)。

## SQL vs NoSQL vs 檔案儲存

| 選項 | 適合 | 不適合 |
| --- | --- | --- |
| SQL 資料庫 | 交易、複雜查詢、強調一致性與完整性 | 巨量非結構化檔案 |
| NoSQL | 高吞吐、彈性 schema（document、key-value、graph、time-series） | 需要多表 join 與嚴格一致性 |
| 檔案儲存 | 原始資料落地、大檔保存 | 需要索引、權限細分、併發更新 |

NoSQL 不是「SQL 的升級版」，而是資料模型或延遲需求不適合關聯式設計時的替代方案，見 [NoSQL 基礎](../databases/nosql-foundations.md)。SQL 在資料工程中多用於建立與維護 table / schema，在分析中多用於查詢與聚合。

## Catalog：讓資料找得到、看得懂

資料一多，就需要 data catalog 回答：這份資料從哪來？誰在用？欄位代表什麼？多久更新一次、品質如何？沒有 catalog，資料會很快變成只有少數人看得懂的黑盒子，詳見 [資料治理](governance.md)。

## 常見陷阱

| 陷阱 | 後果 | 做法 |
| --- | --- | --- |
| 直接覆寫原始檔 | 轉換有錯時無法重跑 | raw 區唯讀，轉換結果寫到另一層 |
| 大表存 CSV | 每次讀取都重新解析、型別飄移 | 落地後轉 Parquet，保留 schema |
| 檔案沒有記錄參考基因體版本 | GRCh37 / GRCh38 座標混用 | 版本寫進檔名或 metadata |
| 小檔案過多（數萬個 KB 級 Parquet） | 讀取 overhead 大於計算 | 合併成 100 MB–1 GB 級檔案（Delta `OPTIMIZE`） |
