[Data Science](../README.md) › [Data Engineering](README.md) › 處理與 Pipeline

# 處理與 Pipeline (Processing and Pipelines)

Pipeline 把資料從一個系統穩定搬到另一個系統，並在途中完成清理、轉換與交付。它和一次性分析腳本的差別不在程式多複雜，而在於：明天能不能自動再跑一次、來源改了格式會不會被發現、下游是否每次都拿到一致的結果。

| 一次性分析問 | Pipeline 問 |
| --- | --- |
| 這次能不能算出答案？ | 明天還能不能穩定重跑？ |
| 結果對不對？ | 來源延遲或改格式時怎麼辦？重跑會不會重複寫入？ |
| — | 下游是不是每次都拿到同樣結構的資料？ |

## ETL 與 ELT

ETL（Extract → Transform → Load）是最常見的資料移動框架；pipeline 是更廣的概念，涵蓋資料如何在多個系統之間移動與協調。

| 模式 | 流程 | 常見場景 | 優點 | 限制 |
| --- | --- | --- | --- | --- |
| ETL | 擷取 → 轉換 → 載入 | 在外部程式先整理，再載入目標；來源含非表格資料 | 目標端儲存少；可在載入前去除個資 | 轉換規則改了要重新擷取；需要另外的運算環境 |
| ELT | 擷取 → 載入 → 轉換 | 先載入 warehouse / lakehouse，再用平台算力轉換 | 原始資料在平台內，可隨時重跑轉換；適合雲端擴充 | 原始資料佔空間；個資控管要在平台內做好 |

| 階段 | 內容 | 檢查點 |
| --- | --- | --- |
| Extract | 從資料庫、檔案、API、網頁取出資料 | 列數、檔案 checksum、來源時間範圍 |
| Transform | 清理錯誤值、合併來源、計算指標、展平 JSON、建特徵表 | schema、型別、缺值比例、key 唯一性 |
| Load | 寫入分析表、dashboard 後端、feature table | 寫入列數、寫入策略（append / replace / upsert）、主鍵與時間欄 |

> 轉換結果寫到另一層，不要覆寫原始資料；規則改了才能從原始資料重跑。

## Batch vs Stream

| | Batch | Event-triggered | Stream |
| --- | --- | --- | --- |
| 觸發 | 固定時間或累積一定量 | 某事件發生（新檔案到達） | 持續處理沒有終點的事件流 |
| 每次執行 | 有明確起訖，稱為一個 job | 一次性 job | 長時間運作的服務 |
| 延遲 | 分鐘到天 | 秒到分鐘 | 毫秒到秒 |
| 例子 | 每日報表、夜間彙總、定序資料批次處理 | 定序 run 完成後自動啟動 demultiplexing | 即時監控、感測器、clickstream |
| 複雜度 | 低 | 中 | 高 |

event-triggered 不等於 streaming：很多系統只是事件觸發的 batch。只有延遲真的重要時才值得做 streaming，見 [串流處理](streaming.md)。

## 排程與編排 (Scheduling vs Orchestration)

| | Scheduling | Orchestration |
| --- | --- | --- |
| 關心 | 什麼時候觸發 | 多個任務的順序、依賴、重試、失敗處理 |
| 比喻 | 發車時間表 | 整個運輸系統的調度 |
| 工具 | cron、雲端排程器 | Airflow、Dagster、Prefect；生資常用 Nextflow、Snakemake |

編排工具的核心概念是 task（執行單位）、dependency（先後順序）與 DAG（有向無環圖）。價值在於協調多個 job、自動重試、記錄每次執行，以及在失敗時知道從哪一步重跑。Airflow 見 [Airflow](../../computing/workflow-engines/airflow/README.md)，Nextflow 見 [Nextflow](../../computing/workflow-engines/nextflow/README.md)。

| 工具類型 | 適合 |
| --- | --- |
| Airflow / Dagster / Prefect | 定時的資料擷取與轉換、跨系統的 ETL |
| Nextflow / Snakemake | 以檔案為單位的生資分析流程、HPC / 雲端批次、容器化工具 |
| dbt | warehouse 內的 SQL 轉換，見 [dbt](dbt-foundations.md) |

## 冪等與重跑 (Idempotency)

冪等的 pipeline 對同一輸入重跑多次，結果和跑一次相同。這是能安全重試與補跑 (backfill) 的前提。

| 寫法 | 冪等？ | 說明 |
| --- | --- | --- |
| 每次 `append` 整批結果 | 否 | 重跑一次資料就重複 |
| 先刪除該分區再寫入（`DELETE WHERE date = :d` + `INSERT`，或覆寫該日期分區） | 是 | 最常見的批次寫法 |
| `MERGE` / upsert 依主鍵更新 | 是 | 適合增量更新 |
| 輸出檔名含執行時間戳 | 否 | 重跑產生多份，下游不知道讀哪份 |

```python
# 以「處理日期」為參數、覆寫該日期分區：重跑或補跑任何一天都安全
def run(day: str):
    raw = extract(day)                       # 只取該日資料
    out = transform(raw)
    assert out["sample_id"].is_unique
    out.to_parquet(f"curated/date={day}/part.parquet")   # 同一路徑覆寫
```

## 常見轉換操作

| 操作 | pandas | PySpark | SQL |
| --- | --- | --- | --- |
| 刪除空白 / 全缺值列 | `dropna(how="all")` | `df.na.drop(how="all")` | `WHERE ... IS NOT NULL` |
| 去重 | `drop_duplicates()` | `dropDuplicates()` | `DISTINCT`、`ROW_NUMBER()` |
| 取代錯誤值 | `replace()` | `replace()`、`when().otherwise()` | `CASE WHEN` |
| 修正型別 | `astype()`、`pd.to_datetime()` | `cast()` | `CAST()` |
| 篩選 | `query()`、布林索引 | `filter()` / `where()` | `WHERE` |
| 聚合 | `groupby().agg()` | `groupBy().agg()` | `GROUP BY` |
| 合併 | `merge()` | `join()` | `JOIN` |

型別整理要在早期做：型別不對，後面的 join、篩選、聚合都可能出現難追的錯誤（例如 `"001"` 與 `1` 對不上）。join 後一定檢查列數、未配對的 key 與重複放大。

平台常同時提供三種轉換介面：低程式碼（Dataflows / Power Query）、SQL、Spark notebook。選哪個看資料量、團隊技能、是否需要版本控制與重用，而不是個人偏好；三者可以在同一條流程的不同層並存。

## Spark 上的 pipeline

1. 用明確的 schema 讀入 CSV / JSON / 資料庫
2. 用 `filter()`、`withColumn()`、`drop()` 清理與轉換
3. 中途檢查 schema、列數與關鍵規則
4. 必要時把中間結果寫成 Parquet
5. 輸出到檔案、資料庫或下游分析

| 髒資料 | Spark 讀 CSV 的處理 |
| --- | --- |
| 註解列 | `comment="#"` |
| 首列是欄名 | `header=True`；已給 schema 時不要再依賴推斷 |
| 欄內又有分隔資料 | 先讀成單欄，再用 `split()` 二次解析 |
| 欄位數不一致 | `mode="DROPMALFORMED"` 或 `PERMISSIVE` + `columnNameOfCorruptRecord` 收集壞列 |

API 細節見 [Spark 與 PySpark](spark.md)。

## 測試 Pipeline

| 層級 | 檢查什麼 | 工具 |
| --- | --- | --- |
| 單元測試 | 把 extract / transform / load 拆成函式，驗證型別、欄位、轉換規則 | `pytest`，見 [測試](../python-foundations/testing.md) |
| 檢查點驗證 | 擷取後列數合理、轉換後 schema 正確、載入前後一致 | assert、[pandera / Great Expectations](data-quality-checks.md) |
| 端對端測試 | 整條流程從來源跑到目的地，重複執行結果穩定，下游取得到 | 測試環境 + 小型固定資料集 |

測試環境與正式環境要分開，否則驗證本身就可能污染正式資料；人工 spot check 也優先在測試資料或 staging 進行。

## 轉換前後做 profiling

轉換不是「成功執行」就好，要確認資料真的變得更可用：

| 訊號 | 異常例子 |
| --- | --- |
| 列數 | join 後暴增（key 不唯一）或驟減（key 格式不一致） |
| 缺值比例 | 某欄突然全是缺值（上游改了欄名） |
| distinct 數 | 類別數變多（大小寫、空白不一致） |
| 分布 | 數值量級改變（單位換了） |
| 型別 | 數字欄變成字串（混入 `"N/A"`） |

## 平行與雲端處理

| | 好處 | 代價 |
| --- | --- | --- |
| 平行處理 | 吞吐量高、處理快 | 協調成本、失敗模式複雜、不是每個任務都能拆 |
| 雲端處理 | 依需求租用與擴充、不必維護硬體 | 長期成本、vendor lock-in、資料搬移費用（egress） |

資料大到記憶體放不下時，先想怎麼切分與合併部分結果，而不是先想語法，見 [超出記憶體的處理](scalable-processing-and-out-of-core.md)。
