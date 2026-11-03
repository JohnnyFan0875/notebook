[Computing](../README.md) › [工作流引擎](README.md) › Airflow

# Apache Airflow

Airflow 是用 Python 程式碼描述工作流的編排平台 (orchestrator)：把任務拆分、依賴、排程、等待條件、重試與監控放進同一個可觀察、可重跑的系統。適合定時的批次資料 pipeline（每天從 API 擷取 → 清理 → 寫入倉儲 → 產報表）；生資的檔案導向分析流程通常用 [Nextflow](nextflow/README.md) 或 [Snakemake](snakemake.md)。ETL / ELT、冪等與重跑的概念見 [處理與 Pipeline](../../data-science/data-engineering/processing-and-pipelines.md)。

| 適合 | 不適合 |
| --- | --- |
| 定時批次 ETL / ELT、多步驟且有依賴 | 低延遲串流（用 Kafka、Flink） |
| 需要重試、補跑歷史日期 (backfill)、監控 | 大量極短的事件驅動任務 |
| 已有很多獨立腳本，缺少統一編排 | 單一 shell 腳本就能搞定的事（用 [cron](../operating-system/command-line-data-processing.md#排程cron)） |
| 協調其他系統（Spark、dbt、資料庫、雲端服務） | 本身做大量資料轉換（Airflow 是指揮，不是引擎） |

> 本篇以 **Airflow 3**（2025 年 4 月發布）的寫法為主：`DAG` 等從 `airflow.sdk` 匯入、`schedule_interval` 改為 `schedule`、內建 operator 移到 `standard` provider、SLA 功能移除。舊版程式碼可用 `ruff check dags/ --select AIR3` 找出需要修改之處。

## 核心概念

| 概念 | 意義 |
| --- | --- |
| DAG | 有向無環圖：一個工作流的所有任務與先後關係，加上排程 |
| Task | DAG 中的一個節點，一個執行單位 |
| Operator | 任務的範本（做什麼類型的事）；task 是 operator 的實例 |
| Dependency | 任務之間的順序：`a >> b` 表示 a 完成後才跑 b |
| DAG run | DAG 的一次執行，對應一個邏輯日期 (logical date) |
| Scheduler / Worker | 決定何時執行 / 實際執行任務 |

> 每個 task 獨立執行，可能在不同機器上；不要假設 task 之間共享記憶體或本機檔案。小量資料用 XCom 傳遞，大量資料寫到共享儲存（S3、資料庫）再傳路徑。

## 範例

```python
# dags/sales_report.py
from datetime import datetime, timedelta

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.filesystem import FileSensor

default_args = {                               # 所有 task 共用的參數
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sales_report",
    schedule="0 6 * * *",                      # 每天 06:00（cron 語法；也可用 "@daily"、None = 只手動觸發）
    start_date=datetime(2024, 1, 1),
    catchup=False,                             # 不自動補跑 start_date 以來錯過的所有日期
    default_args=default_args,
    tags=["reporting"],
) as dag:
    start = EmptyOperator(task_id="start")     # 結構上的起點，不做事

    wait_for_file = FileSensor(                # 感測器：等條件成立才往下
        task_id="wait_for_file",
        filepath="/data/incoming/sales_{{ ds }}.csv",   # {{ ds }}：此次執行的邏輯日期 YYYY-MM-DD
        poke_interval=300,                     # 每 5 分鐘檢查一次
        timeout=6 * 60 * 60,                   # 最多等 6 小時，超過就失敗
        mode="reschedule",                     # 等待期間釋放 worker slot
    )

    @task                                      # TaskFlow API：一般 Python 函式變成 task
    def clean(ds=None):
        import pandas as pd
        df = pd.read_csv(f"/data/incoming/sales_{ds}.csv")
        out = f"/data/clean/sales_{ds}.parquet"
        df.dropna(subset=["amount"]).to_parquet(out)
        return out                             # 回傳值自動存成 XCom，傳給下游

    @task
    def summarize(path: str):
        import pandas as pd
        return float(pd.read_parquet(path)["amount"].sum())

    notify = BashOperator(
        task_id="notify",
        bash_command='echo "Report for {{ ds }} done"',   # Jinja 模板
    )

    cleaned = clean()
    start >> wait_for_file >> cleaned          # 依賴關係
    summarize(cleaned) >> notify               # 傳遞回傳值也會自動建立依賴
```

| Operator / 寫法 | 用途 |
| --- | --- |
| `@task`（TaskFlow） | 執行 Python 函式，回傳值自動傳遞；新程式碼首選 |
| `PythonOperator` | 舊式寫法：`PythonOperator(task_id=..., python_callable=f)` |
| `BashOperator` | 執行 shell 指令或腳本、呼叫 CLI 工具 |
| `EmptyOperator` | 起點、終點、分支匯合的佔位 |
| Provider operators | 各系統的整合：`SQLExecuteQueryOperator`、Spark、dbt、AWS / GCP / Azure、Kubernetes |

### 依賴寫法

```python
a >> b >> c          # a → b → c
a >> [b, c] >> d     # b、c 平行，都完成後才跑 d
c << b               # 等同 b >> c
```

## 排程

| 概念 | 說明 |
| --- | --- |
| `schedule` | cron 字串、`"@daily"` 等 preset、`timedelta`、資料集 / asset 觸發，或 `None`（只手動） |
| `start_date` | 排程從何時開始計算，**不是**「立刻開始執行」 |
| 邏輯日期 (`{{ ds }}`) | 這次執行「負責處理」的資料日期；每日 DAG 在 1/2 的執行通常處理 1/1 的資料區間 |
| `catchup` | `True` 時會補跑 `start_date` 到現在所有錯過的區間；多數情況設 `False` |
| backfill | 手動補跑指定區間：`airflow backfill create --dag-id sales_report --from-date 2024-01-01 --to-date 2024-01-07` |

> DAG 沒有如預期執行時，先檢查 `start_date` 是否合理、是否至少已經過了一個排程區間、DAG 是否在 UI 中被暫停 (paused)。

任務要能**冪等 (idempotent)**：以邏輯日期為參數、覆寫該日期的輸出分區，重跑或補跑任何一天都安全。

## 感測器 (Sensors)

感測器不做工作本身，而是阻止工作流太早往下跑：等檔案出現、等資料庫有紀錄、等 API 回應某個狀態（`HttpSensor`）、等另一個 DAG 完成（`ExternalTaskSensor`）。

| 參數 | 說明 |
| --- | --- |
| `mode="poke"` | 預設；持續佔用 worker slot，定期檢查 |
| `mode="reschedule"` | 檢查之間釋放 slot；等待時間長時使用 |
| `poke_interval` | 檢查間隔（秒） |
| `timeout` | 最多等多久，超過即失敗 |
| deferrable operators | 等待交給 triggerer 程序，更省資源（新版建議） |

## 模板 (Jinja)

```python
BashOperator(
    task_id="process",
    bash_command="python process.py --date {{ ds }} --file {{ params.filename }}",
    params={"filename": "file1.txt"},
)
```

| 常用變數 | 意義 |
| --- | --- |
| `{{ ds }}` / `{{ ds_nodash }}` | 邏輯日期 `2024-01-01` / `20240101` |
| `{{ data_interval_start }}` / `{{ data_interval_end }}` | 此次執行負責的資料區間 |
| `{{ params.x }}` | 自訂參數 |
| `{{ var.value.x }}` | Airflow Variable |

模板讓同一個 task 定義依日期、參數重用，避免複製貼上多個幾乎相同的 task；但不要把複雜商業邏輯藏在 Jinja 字串中。

## 本機執行與除錯

```bash
uv pip install "apache-airflow==3.*"     # 正式安裝應依官方說明使用 constraints 檔
airflow standalone                       # 本機啟動所有元件與 UI（http://localhost:8080），僅供開發
airflow dags list
airflow dags list-import-errors          # DAG 沒出現時：看匯入錯誤
python dags/sales_report.py              # 確認檔案本身能被 Python 解析
airflow tasks test sales_report clean 2024-01-01   # 單獨執行一個 task，不記錄狀態、不檢查依賴
airflow dags test sales_report 2024-01-01          # 完整跑一次 DAG
```

| 實務守則 | 原因 |
| --- | --- |
| DAG 檔案頂層不做重運算或連線 | scheduler 會頻繁解析 DAG 檔；import 放進 task 內 |
| task 冪等、以日期參數化 | 安全重跑與補跑 |
| task 大小適中 | 太大難以重試，太碎管理成本高 |
| 資料不經過 XCom | XCom 只傳小量 metadata（路徑、計數） |
| 機密用 Connections / Variables 或 secrets backend | 不寫在 DAG 程式碼中 |

| 替代方案 | 特色 |
| --- | --- |
| Dagster | 以資料資產 (asset) 為中心、型別與測試友善 |
| Prefect | 純 Python、動態工作流、上手快 |
| 雲端託管 | Amazon MWAA、Google Cloud Composer、Astronomer：託管的 Airflow |
