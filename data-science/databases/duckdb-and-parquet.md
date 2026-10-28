[Data Science](../README.md) › [Databases](README.md) › DuckDB 與 Parquet

# DuckDB 與 Parquet

DuckDB 是嵌入式的分析型資料庫：`pip install duckdb` 就能用，不需要伺服器，直接以 SQL 查詢 CSV、Parquet、JSON 檔與記憶體中的 pandas / Polars DataFrame。欄式執行、多執行緒、資料大於記憶體時自動寫入磁碟暫存，筆電上就能處理數十 GB 的表格。Parquet 格式本身與 pandas 讀寫見 [記憶體與儲存格式](../python-foundations/pandas/memory-and-storage.md#parquet)。

## 什麼時候用

| 工具 | 定位 | 適合 |
| --- | --- | --- |
| pandas | 記憶體內的 DataFrame | 資料放得進記憶體、需要逐步互動處理 |
| **DuckDB** | 單機、嵌入式、OLAP（欄式） | 大型檔案的過濾 / join / 聚合；想用 SQL；不想架伺服器 |
| SQLite | 單機、嵌入式、OLTP（列式） | 應用程式或工具內建的小型資料庫、頻繁單筆讀寫 |
| PostgreSQL | 伺服器、OLTP | 多人同時寫入、交易、權限 |
| Spark | 分散式 | 單機處理不了的資料量（見 [Spark](../data-engineering/spark.md)） |

典型生資用途：合併數百個樣本的計數表、查詢整個 cohort 的變異位點表、把 GTF / VCF 匯出的表格與樣本 metadata join，只把結果讀進 pandas。

## Python：查檔案與 DataFrame

```python
import duckdb
import pandas as pd

# 1. 直接查檔案：FROM 後面放路徑（支援萬用字元）
duckdb.sql("SELECT * FROM 'expr_s1.csv' LIMIT 5")
duckdb.sql("FROM 'counts/*.parquet' WHERE sample = 's1'")            # 可省略 SELECT *

# 2. 查 pandas DataFrame：直接用變數名稱，不必先匯入
meta = pd.DataFrame({"sample": ["s1", "s2"], "group": ["case", "ctrl"]})
res = duckdb.sql("""
    SELECT m.group, e.gene, avg(e.tpm) AS mean_tpm
    FROM 'expr_*.csv' AS e
    JOIN meta AS m USING (sample)
    GROUP BY ALL                                   -- 自動以所有非聚合欄分組
""")

# 3. 結果轉出
res.df()            # pandas
res.pl()            # Polars
res.fetchall()      # list of tuples
res.show()          # 印出表格

# 4. 參數化查詢（不要用 f-string 拼值）
duckdb.execute("SELECT * FROM 'expr_s1.csv' WHERE tpm > ? AND gene = ?", [5, "TP53"]).df()
```

### 讀取選項

```python
duckdb.sql("""
    SELECT *
    FROM read_csv('expr_*.csv',
                  union_by_name = true,   -- 各檔欄位不同時依欄名對齊，缺的補 NULL
                  filename = true,        -- 加一欄來源檔名（追蹤樣本來源）
                  types = {'sample': 'VARCHAR'},   -- 指定型別，避免 "001" 被當成整數
                  nullstr = 'NA')
""")

duckdb.sql("DESCRIBE SELECT * FROM 'expr_s1.csv'")    # 自動推斷的欄位型別
duckdb.sql("SUMMARIZE SELECT * FROM 'expr_s1.csv'")   # 每欄的 min / max / 唯一值數 / 缺值比例，快速 EDA
```

| 來源 | 函式 |
| --- | --- |
| CSV / TSV（自動偵測分隔符、標題、型別） | `read_csv('f.tsv')`；`.gz` 壓縮直接讀 |
| Parquet | `read_parquet('dir/**/*.parquet', hive_partitioning = true)` |
| JSON / NDJSON | `read_json('f.json')` |
| Excel | `read_xlsx('f.xlsx', sheet = 'Sheet1')`（excel extension） |
| HTTP / S3 | `FROM 'https://.../f.parquet'`、`'s3://bucket/...'`（httpfs extension，自動載入） |
| SQLite / PostgreSQL 資料庫 | `ATTACH 'db.sqlite' AS s (TYPE sqlite)`、`ATTACH 'dbname=x' AS pg (TYPE postgres)` |

## 寫成 Parquet

```python
# 查詢結果直接寫成 Parquet，不經過 pandas
duckdb.sql("""
    COPY (SELECT * FROM read_csv('counts/*.tsv', filename = true))
    TO 'counts.parquet' (FORMAT parquet, COMPRESSION zstd)
""")

# 依欄位分區：產生 expr_pq/chrom=chr1/...、expr_pq/chrom=chr2/...
duckdb.sql("""
    COPY (SELECT * FROM 'expr.csv')
    TO 'expr_pq' (FORMAT parquet, PARTITION_BY (chrom), OVERWRITE_OR_IGNORE)
""")

# 讀分區資料：篩選分區欄時只讀對應資料夾（partition pruning）
duckdb.sql("""
    SELECT gene, avg(tpm) AS mean_tpm
    FROM read_parquet('expr_pq/**/*.parquet', hive_partitioning = true)
    WHERE chrom = 'chr17'
    GROUP BY ALL
""")
```

Parquet 是欄式格式：只讀查詢用到的欄（projection pushdown），並依 row group 的 min / max 統計跳過不符合 `WHERE` 的區塊（filter pushdown）。CSV 每次都要從頭解析整個檔案。把原始 CSV 轉一次 Parquet，之後的查詢通常快一個數量級以上，檔案也小好幾倍。

## 資料庫檔與記憶體

```python
con = duckdb.connect("analysis.duckdb")        # 持久化的資料庫檔；不給路徑 = 記憶體資料庫
con.execute("CREATE OR REPLACE TABLE expr AS SELECT * FROM 'expr_*.csv'")
con.execute("SELECT count(*) FROM expr WHERE tpm > ?", [5]).fetchone()
con.execute("SET memory_limit = '8GB'")         # 預設約為實體記憶體的 80%
con.execute("SET threads = 4")                  # HPC 上設成分配到的核心數，不要用整台節點的核心數
con.execute("SET temp_directory = '/scratch/duckdb_tmp'")   # 超出記憶體時的暫存位置
con.close()
```

| 注意 | 說明 |
| --- | --- |
| 單一寫入者 | 同時只能有一個程序以讀寫模式開啟同一個 `.duckdb` 檔；多個程序只讀時用 `duckdb.connect(path, read_only=True)` |
| 不是 OLTP | 大量單筆 `INSERT` / `UPDATE` 很慢；批次載入（`COPY`、`CREATE TABLE AS`）才是正確用法 |
| 交換格式 | 不同版本間的 `.duckdb` 檔不一定相容；長期保存與分享用 Parquet |
| 可重現 | 查詢檔案的 SQL 寫進腳本，比互動式匯入再操作容易重跑 |

## 好用的 SQL 擴充

| 語法 | 作用 |
| --- | --- |
| `SELECT * EXCLUDE (col)` / `REPLACE (expr AS col)` | 選除了某欄以外的全部 / 替換某欄 |
| `GROUP BY ALL`、`ORDER BY ALL` | 自動以所有非聚合欄分組 / 排序 |
| `QUALIFY` | 過濾 window function 結果（每組 top-N，見 [Window Functions](sql-window-functions.md#每組-top-n-與去重)） |
| `PIVOT` / `UNPIVOT` | 長寬轉換 |
| `COLUMNS('^tpm_')` | 用 regex 一次對多欄套運算：`SELECT max(COLUMNS('^tpm_'))` |
| `list`、`struct` 型別 | 巢狀資料；`unnest()` 展開 |
| `//` | 整數除法（`/` 一律回傳小數） |

```sql
-- 寬表（基因 × 樣本）轉長表
UNPIVOT counts_wide
ON COLUMNS(* EXCLUDE (gene))
INTO NAME sample VALUE count;
```

## 區間 JOIN：基因組座標

「哪些變異位點落在哪個基因內」是範圍條件的 join。DuckDB 對不等式 join 有專門的演算法（IEJoin），不需要先產生笛卡兒積。

```sql
-- genes：BED 格式（0-based、半開區間 [start, end)）
-- variants：VCF 格式（1-based 位置）
SELECT v.id, v.pos, g.name
FROM variants AS v
JOIN genes    AS g
  ON v.chrom = g.chrom
 AND v.pos >  g.start        -- BED start 是 0-based，1-based 位置要 > start
 AND v.pos <= g."end";       -- end 是保留字，要加引號
```

| 格式 | 座標系統 | 第一個鹼基 | 區間 |
| --- | --- | --- | --- |
| BED、BAM 內部、Python 切片 | 0-based | 0 | 半開 `[start, end)` |
| VCF、GTF / GFF、SAM 文字、UCSC 瀏覽器顯示 | 1-based | 1 | 閉區間 `[start, end]` |

> 座標系統混用是最常見的 off-by-one 錯誤：位置剛好在基因邊界的變異會被算錯。join 前先確認兩邊的格式。大規模區間運算（overlap、最近基因、合併區間）用專門工具更方便：bedtools、`pyranges`（Python）、`GenomicRanges`（R / Bioconductor）。

## R

```r
library(DBI)
library(dplyr)

con <- dbConnect(duckdb::duckdb())                       # 記憶體資料庫；持久化給 dbdir = "x.duckdb"
dbGetQuery(con, "SELECT gene, avg(tpm) FROM 'expr_*.csv' GROUP BY ALL")

# dplyr 語法，由 dbplyr 翻譯成 SQL 在 DuckDB 執行；collect() 才取回 R
tbl(con, sql("SELECT * FROM read_parquet('expr_pq/**/*.parquet', hive_partitioning = true)")) |>
  filter(chrom == "chr17") |>
  summarise(mean_tpm = mean(tpm), .by = gene) |>
  collect()

dbDisconnect(con)
```

`arrow::open_dataset()` 開啟的資料集也能用 `arrow::to_duckdb()` 交給 DuckDB 查詢。R 的匯入流程見 [匯入資料（R）](../r-foundations/importing-data.md#parquet-與大於記憶體的資料)；Python 端另一個選擇是 [Polars](../python-foundations/performance-and-scaling/polars.md) 的 `scan_parquet`。
