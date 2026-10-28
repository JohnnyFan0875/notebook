[Data Science](../README.md) › [Databases](README.md) › 資料庫設計原則

# 資料庫設計原則 (Database Design Principles)

設計資料庫的第一個問題不是用哪個 DBMS，而是「資料要拿來做什麼」：支援日常寫入（交易）還是支援分析，決定了 schema 的形狀、正規化程度、要不要 view、權限怎麼分。

## OLTP vs OLAP

| 面向 | OLTP（交易處理） | OLAP（分析處理） |
| --- | --- | --- |
| 目的 | 支援日常作業：下單、登錄檢體、更新狀態 | 報表與分析：趨勢、彙總、跨主題比較 |
| 查詢 | 簡單、頻繁、讀寫少量列 | 複雜、聚合大量列、以讀為主 |
| 資料 | 最新狀態 | 整合後的歷史資料 |
| 設計 | 以應用程式為中心、正規化 | 以主題為中心、dimensional model（星狀） |
| 重視 | 寫入一致性、交易、低延遲 | 掃描與聚合效率 |
| 典型系統 | PostgreSQL、MySQL、SQL Server | Snowflake、BigQuery、Redshift、DuckDB |

例：LIMS / EHR 是 OLTP（每次檢驗結果即時寫入）；研究用的資料倉儲把多個來源整合成歷史資料，是 OLAP。直接在 OLTP 系統上跑大量分析查詢，會拖慢日常作業；常見做法是定期 ETL 到分析用的資料庫（見 [Processing and Pipelines](../data-engineering/processing-and-pipelines.md)）。

## 設計的層次

| 層次 | 回答 | 產出 |
| --- | --- | --- |
| 概念模型 (conceptual) | 有哪些實體、彼此怎麼關聯？ | ER diagram：病人、檢體、定序批次、檢驗 |
| 邏輯模型 (logical) | 有哪些表、欄位、key、關係？ | 正規化的關聯模型或星狀模型 |
| 實體模型 (physical) | 用什麼型別、index、分區、儲存？ | `CREATE TABLE`、`CREATE INDEX` |

## Schema 與欄位型別

schema 是資料庫的藍圖：表、欄位、關係、index、view、constraint。關聯式資料庫是 **schema-on-write**：寫入前就要符合結構；資料湖與 NoSQL 偏 **schema-on-read**：讀取時才解析結構。

欄位型別定義了欄位的 domain（可以放什麼值、能做哪些運算）：

```sql
CREATE TABLE samples (
  sample_id     TEXT PRIMARY KEY,          -- "S001" 保留前導 0，不用 INTEGER
  patient_id    TEXT NOT NULL REFERENCES patients (patient_id),
  collected_on  DATE NOT NULL,             -- 不存成 '3/1/2024' 字串
  rin           NUMERIC(3, 1) CHECK (rin BETWEEN 0 AND 10),
  is_tumor      BOOLEAN NOT NULL
);
```

| Constraint | 防止 |
| --- | --- |
| `PRIMARY KEY` | 重複與缺 ID |
| `NOT NULL` | 必填欄位留空 |
| `UNIQUE` | 重複值（如 barcode） |
| `CHECK` | 不合理的值（負的數量、RIN > 10） |
| `FOREIGN KEY` | 指向不存在的父資料（孤兒列） |

> 在資料庫層設 constraint，錯誤資料進不來；只在分析時檢查，錯誤已經擴散到下游。

## Key

| 名詞 | 意義 | 例子 |
| --- | --- | --- |
| superkey | 能唯一識別一列的欄位集合（可含多餘欄位） | `(sample_id, collected_on)` |
| candidate key | 最小的 superkey，少一欄就不唯一 | `sample_id`、`barcode` |
| primary key | 選定的 candidate key | `sample_id` |
| composite key | 多欄組成的 key | `(patient_id, visit_date)` |
| natural key | 業務上本來就有的識別碼 | 病歷號、條碼 |
| surrogate key | 系統產生、沒有業務意義的 ID | `GENERATED AS IDENTITY`、UUID |

natural key 可能改變（重新編號、格式調整）或含個資（病歷號），主鍵常改用 surrogate key，natural key 另加 `UNIQUE`。外鍵與被參照的主鍵型別必須一致；型別不同是 schema 開始偏掉的訊號。

## 外鍵與參照完整性

```sql
ALTER TABLE order_items
ADD CONSTRAINT order_items_order_id_fkey
FOREIGN KEY (order_id) REFERENCES orders (id)
ON DELETE CASCADE;
```

| 刪除父資料時（`ON DELETE`） | 行為 | 適合 |
| --- | --- | --- |
| `NO ACTION` / `RESTRICT`（預設） | 擋下刪除 | 歷史紀錄不能消失（檢驗結果） |
| `CASCADE` | 子資料一起刪 | 子資料沒有父資料就無意義（訂單明細） |
| `SET NULL` | 子資料外鍵改為 `NULL` | 保留子資料、解除關聯 |
| `SET DEFAULT` | 改為預設值 | 歸到「未分類」 |

這是資料生命週期的業務決定，不只是語法：明細該不該跟著主資料消失、歷史資料要不要保留。

## 正規化 vs 維度模型

| | 正規化設計 | 維度設計 (dimensional) |
| --- | --- | --- |
| 適合 | OLTP、主資料管理 | OLAP、BI 報表 |
| 目標 | 減少冗餘、避免更新異常 | 查詢直觀、聚合快 |
| 形狀 | 很多小表、多層 join | fact table + dimension tables |
| 細節 | [正規化](database-normalization.md) | [Dimensional Modeling and Star Schema](../data-engineering/dimensional-modeling-and-star-schema.md) |

星狀 (star) 與雪花 (snowflake) schema：

| | Star | Snowflake |
| --- | --- | --- |
| dimension | 一張寬表（反正規化） | 再拆成多層（正規化） |
| 查詢 | join 少、直觀，BI 工具友善 | join 多 |
| 冗餘 | 較多 | 較少 |
| 選擇 | 分析與報表的預設 | dimension 很大且需要獨立維護時 |

## View

view 是存起來的查詢，查它就像查一張表，但不另存資料。

```sql
CREATE VIEW tumor_samples AS
SELECT s.sample_id, s.collected_on, p.sex, p.age_at_diagnosis
FROM samples AS s
JOIN patients AS p USING (patient_id)
WHERE s.is_tumor;

SELECT * FROM tumor_samples WHERE collected_on >= '2024-01-01';
```

| 用途 | 注意 |
| --- | --- |
| 封裝常用的 join 與過濾，避免各處重寫 | 每次查詢都重新執行底層查詢，不是效能優化 |
| 提供穩定介面：底層表改名、拆表時 view 不變 | 層層疊的 view 很難除錯與調校 |
| 權限邊界：只開放 view，不開放含個資的原表 | 下游大量依賴很重的 view 時，改成 materialized view 或正式的分析表 |

materialized view（PostgreSQL、Oracle、Snowflake）把結果實際存下來，查詢快，但要定期 `REFRESH MATERIALIZED VIEW` 才會更新。

## 權限是設計的一部分

```sql
CREATE ROLE analyst_role;
GRANT SELECT ON tumor_samples TO analyst_role;     -- 透過 view 開放去識別化後的欄位
REVOKE ALL ON patients FROM analyst_role;          -- 原表不開放
GRANT analyst_role TO alice, bob;                  -- 權限給角色，使用者掛到角色
```

| 原則 | 原因 |
| --- | --- |
| 權限給 role，不直接給個人 | 人員異動時只改成員關係 |
| 最小權限 | 分析人員只需要讀；寫入留給 ETL 帳號 |
| 敏感欄位用 view 或 column-level 權限隔開 | 病歷號、姓名、出生日期等直接識別資訊不外流（見 [Privacy and Regulation](../responsible-ai/privacy-and-regulation.md)） |

PostgreSQL 的實際語法見 [PostgreSQL：psql 與 COPY](postgresql-psql-and-copy.md#角色權限與-schema)。

## 選擇 DBMS

| 工作負載 | 選擇 |
| --- | --- |
| 多人即時寫入、需要交易與 constraint | PostgreSQL、MySQL、SQL Server |
| 單機分析大型檔案、不想架伺服器 | DuckDB（見 [DuckDB 與 Parquet](duckdb-and-parquet.md)） |
| 嵌入應用程式或工具的小型資料庫 | SQLite |
| 大規模歷史資料分析、多人共用 | 雲端資料倉儲（Snowflake、BigQuery） |
| 原始、異質、尚未定義結構的大量資料 | 資料湖（物件儲存 + Parquet） |
| 巢狀文件、key 查詢、關係網路 | NoSQL（見 [NoSQL 基礎](nosql-foundations.md)） |

## 常見錯誤

| 錯誤 | 後果 |
| --- | --- |
| 還沒釐清用途就決定 schema | 寫入與分析兩頭都不好用 |
| 用 OLTP 結構直接承擔大量分析查詢 | 拖慢日常作業，分析也慢 |
| 沒有 constraint，靠應用程式檢查 | 繞過應用程式的匯入（腳本、手動修正）帶進錯誤資料 |
| 把 view 當成設計問題的補丁 | 層層疊加後無法維護 |
| 權限直接發給個人 | 人員異動後殘留權限 |
