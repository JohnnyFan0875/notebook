[Data Science](../README.md) › [Data Engineering](README.md) › 資料擷取

# 資料擷取 (Ingestion)

擷取是把資料從來源系統帶進資料平台的第一步。重點不是「讀得進來」，而是先判斷來源型態、型別與更新方式，並保留原始檔以便日後重跑。Python / R 的讀檔語法細節見 [匯入資料（Python）](../python-foundations/importing-data.md) 與 [匯入資料（R）](../r-foundations/importing-data.md)。

## 擷取前先回答

| 問題 | 影響 |
| --- | --- |
| 來源是檔案、資料庫、API，還是事件流？ | 連線方式、認證、速率限制 |
| 結構化、半結構化還是非結構化？ | 要不要先展平、補 metadata |
| 一次性匯入還是持續更新？ | 全量 vs 增量、排程 |
| 下游是分析、報表、模型，還是只先落地保存？ | 要做多少轉換 |
| 日期、ID、缺值怎麼表示？ | 讀取時就指定，不要盲信自動推斷 |

## 來源型態

| 來源 | 特徵 | 讀取時要確認 |
| --- | --- | --- |
| CSV / TSV | 簡單、易交換；schema 約束弱，欄位品質容易漂移 | 分隔符號、`skiprows`（檔頭說明列）、`usecols` / `nrows` 先縮小範圍、`dtype`、缺值字串 |
| Excel | 多工作表、公式、合併儲存格 | `sheet_name`、標題列位置；多個結構相同的 sheet 先補來源欄再合併 |
| 純文字 | 非結構化，需要 parsing | 編碼、斷行、要抽出哪些欄位 |
| JSON | 半結構化、可巢狀、欄位會隨版本演進 | 外層結構（`orient`）、巢狀欄位在擷取時展平或先原樣落地 |
| Parquet | 欄式、有 schema、壓縮 | 只讀需要的欄（`columns=`） |
| SQL 資料庫 | schema 明確、支援型別與多人存取 | 連線 URI、帳密不寫死、在資料庫端先過濾 |
| Web API | 資料庫之上的一層介面 | 認證、分頁、rate limit、錯誤重試，見 [API 與 HTTP](../python-foundations/api-http.md) |

```python
import pandas as pd

# CSV：讀取時就指定型別與缺值，避免 "001" 變成 1、"NA" 字串變成缺值
meta = pd.read_csv(
    "samples.tsv", sep="\t",
    dtype={"sample_id": "string", "batch": "category"},
    na_values=["", "NA", "-"],
    parse_dates=["collection_date"],   # 格式不標準時改成讀進來後 pd.to_datetime(format=...)
)

# 巢狀 JSON：展平成表格
import json
records = json.load(open("api_response.json"))["results"]
df = pd.json_normalize(records, sep="_")          # {"a": {"b": 1}} → 欄位 a_b

# 資料庫：在資料庫端先過濾，只拉需要的列
from sqlalchemy import create_engine, text
engine = create_engine("postgresql+psycopg://user@host/db")   # 密碼放環境變數或 .pgpass
with engine.connect() as conn:
    labs = pd.read_sql(text("SELECT * FROM labs WHERE visit_date >= :d"), conn,
                       params={"d": "2025-01-01"})
```

SQLite 本身就是一個檔案；PostgreSQL 等伺服器型資料庫需要 driver、帳密與網路權限。對擷取來說差別不在 pandas 語法，而在連線與權限設定，見 [Python 與 SQLAlchemy](../databases/python-sqlalchemy.md)。

## 生資常見的擷取問題

| 問題 | 症狀 | 做法 |
| --- | --- | --- |
| Excel 把基因名轉成日期 | `SEPT2` → `2-Sep`、`MARCH1` → `1-Mar` | 不經 Excel；必須用時先把欄位設為文字；下游以 HGNC 新名稱（`SEPTIN2`）對照 |
| 大型壓縮檔 | `.fastq.gz`、`.vcf.gz` 數十 GB | 串流讀取，不要解壓到記憶體；VCF 用 bgzip + tabix 索引後依區間讀 |
| 檔案傳輸損毀 | 下游解析在中途失敗 | 下載後比對來源提供的 MD5 / SHA256 |
| 樣本 ID 不一致 | metadata 與計數矩陣對不上 | 擷取時就檢查兩邊 ID 集合是否相同，見 [資料品質檢查](data-quality-checks.md) |
| 參考基因體版本不明 | 座標錯位 | 檔名或 metadata 記錄 GRCh37 / GRCh38 與註解版本 |

```bash
# 下載後驗證 checksum（bash；macOS 用 shasum -a 256）
md5sum -c files.md5
sha256sum sample1.fastq.gz

# VCF：壓縮、建索引、只讀某區間
bgzip cohort.vcf && tabix -p vcf cohort.vcf.gz
bcftools view -r chr17:43044295-43125483 cohort.vcf.gz
```

## 全量 vs 增量擷取

| 策略 | 做法 | 適合 | 風險 |
| --- | --- | --- | --- |
| 全量 (full load) | 每次重抓整份 | 小表、來源沒有更新時間欄 | 成本隨資料量增加 |
| 增量 (incremental) | 只抓 `updated_at > 上次水位` 的資料 | 大表、持續更新 | 來源刪除的資料抓不到；時鐘或時區不一致會漏資料 |
| CDC (change data capture) | 讀資料庫的變更日誌 | 需要完整的新增 / 更新 / 刪除 | 需要來源資料庫支援 |

增量擷取要記錄「水位」(high watermark)，並讓重跑同一區間不會重複寫入（冪等），見 [處理與 Pipeline](processing-and-pipelines.md#冪等與重跑-idempotency)。

## 平台內建的擷取工具

雲端平台常把擷取拆成元件：Microsoft Fabric 的 Data Pipelines（編排、排程）、Dataflows Gen2（Power Query Online 的低程式碼轉換，支援 staging 與 refresh）、Shortcuts（邏輯連結，不複製資料）；Databricks 的 Auto Loader 與 Lakeflow Connect；Snowflake 的 stage + `COPY INTO`。使用時要分清楚哪一層是 raw、哪一層是平台自動管理的暫存、哪一層是給下游的 serving。

> 落地 (landing) 階段先保留原始資料，未來轉換規則改了才能重跑；擷取最常見的錯誤不是讀不到，而是型別判錯。
