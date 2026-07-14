# Apache Airflow

Apache Airflow 是用 Python 程式碼描述 workflow 的 orchestration platform。它的核心價值不是「定時跑腳本」而已，而是把：

- 任務拆分
- 依賴關係
- 排程
- 等待條件
- 監控與失敗處理

放進同一套可觀察、可重跑的 workflow system。

## What Airflow Is Really For

如果把 data engineering 理解成「把資料相關動作變成可靠、可重複、可維護的流程」，那 Airflow 做的就是協調這些流程。

Airflow 特別適合：

- batch-style data pipelines
- 多步驟 ETL / ELT
- 需要依賴管理與重試的工作流
- 已經有很多獨立腳本，但缺少統一 orchestration 的團隊

它不一定適合：

- 超低延遲 streaming
- 每個 task 都極短且事件量極高的工作
- 只需要單一 shell script 的極簡自動化

## Core Mental Model

可以先把 Airflow 拆成四個基本概念：

1. `DAG`
2. `task`
3. `operator`
4. `dependency`

## DAG

`DAG` 是 Directed Acyclic Graph，用來描述一個 workflow 的任務集合與先後順序。

它的重要性不只是圖形結構，而是：

- 哪些 task 屬於同一個 workflow
- 哪些 task 必須先完成
- 這個 workflow 何時應該被排程

一個最小範例可以長這樣：

```python
from airflow import DAG

etl_dag = DAG(
    dag_id="etl_pipeline",
    default_args={"start_date": "2024-01-08"},
)
```

更常見的寫法是 context manager：

```python
from airflow import DAG

with DAG("etl_workflow", default_args=default_arguments) as etl_dag:
    ...
```

這種寫法通常比較乾淨，因為 task 會自然掛進這個 DAG context。

## Tasks and Operators

在 Airflow 裡，一個 `task` 代表 workflow 中的一個執行單位，而 task 通常是由某個 `operator` 實例化出來的。

教材裡有一個很重要的提醒：

Key point: operator 是 task template，task 是實際放進 DAG 裡的那個節點。

operator 的一般特徵包括：

- 代表單一工作
- 通常獨立執行
- 不應該假設和其他 task 任意共享記憶體或程序狀態

### EmptyOperator

`EmptyOperator` 常用來做邏輯上的起點、終點或中間佔位。

```python
from airflow.operators.empty import EmptyOperator

start = EmptyOperator(task_id="start")
```

它本身不做實際業務工作，但可以讓 DAG 結構更清楚。

### BashOperator

`BashOperator` 適合執行 shell command 或 shell script。

```python
from airflow.operators.bash import BashOperator

bash_task = BashOperator(
    task_id="bash_example",
    bash_command='echo "Example!"',
)
```

適合：

- 呼叫既有 shell script
- 啟動 CLI 工具
- 做簡單檔案處理或系統命令

但如果邏輯已經大量依賴 Python 物件操作，通常 `PythonOperator` 會更自然。

### PythonOperator

`PythonOperator` 適合直接執行 Python callable。

```python
from airflow.operators.python import PythonOperator

python_task = PythonOperator(
    task_id="simple_print",
    python_callable=print_hello,
)
```

這很適合：

- 包裝既有 Python function
- 做較複雜的資料處理邏輯
- 在 task 中直接呼叫 Python library

## Task IDs Matter

每個 task 都需要 `task_id`，因為 Airflow 會用它來：

- 在 UI 中辨識 task
- 在 CLI 中定位 task
- 表示依賴圖上的節點名稱

所以 `task_id` 最好：

- 穩定
- 可讀
- 反映工作內容

## Dependencies

Airflow 的依賴關係通常用 `>>` 和 `<<` 來表達。

```python
task1 >> task2
task2 >> task3 >> task4
task1 >> task2 << task3
```

心智模型上：

- `task1 >> task2` 表示 `task1` 必須先完成
- `task2 << task1` 是同一件事的反向寫法

這種寫法的優點是 DAG 結構可以直接從程式碼讀出來。

## Scheduling

Airflow 不只負責描述 workflow，也負責決定 workflow 何時被觸發。

關鍵欄位通常是：

- `start_date`
- `schedule_interval`

`schedule_interval` 可以代表：

- 固定時間週期，例如每天、每小時
- 手動觸發型 DAG
- 某些特殊 preset

Key point: 很多人第一次碰 Airflow 時，會把 `start_date` 理解成「立即開始跑」。但實際上 scheduler 邏輯通常是從 `start_date` 與 `schedule_interval` 一起推導執行時點。

因此如果 DAG 沒有出現在預期執行狀態，先檢查：

- `start_date` 是否合理
- 至少一個 `schedule_interval` 是否已經過去

## Manual Testing and Basic Debugging

Airflow 入門時，很值得先熟悉幾個基礎檢查方式。

### Test a Single Task

```bash
airflow tasks test <dag_id> <task_id> [execution_date]
```

這很適合：

- 單獨驗證某個 task 的邏輯
- 不想等整個 DAG 跑起來才看結果
- 排查 task 內部程式是否能成功執行

### If a DAG Does Not Show Up

如果 DAG 沒出現在 `airflow dags list`，常見檢查方向是：

```bash
airflow dags list-import-errors
python3 <dagfile.py>
```

這兩個步驟通常很有效，因為它們直接在問：

- Airflow import DAG file 時有沒有出錯
- 這份 Python 檔案本身能不能成功被解析

## Sensors

`sensor` 是一種會等待條件成立的 operator。

它的用途包括：

- 等檔案出現
- 等資料庫紀錄到位
- 等某個 HTTP response 滿足條件

可以先把 sensor 理解成：

Key point: 不是做工作本身，而是阻止 workflow 太早往下跑。

### Common Sensor Arguments

教材裡最值得留下的是這幾個參數：

- `mode`
- `poke_interval`
- `timeout`

#### `mode="poke"`

預設模式。task 會持續占著 worker slot，定期檢查條件是否成立。

#### `mode="reschedule"`

會先釋放 worker slot，之後再回來檢查。

這在等待時間可能很長時更重要，因為它比較不會浪費執行資源。

#### `poke_interval`

多久檢查一次條件。

#### `timeout`

最多等多久，超過就 fail。

### FileSensor

```python
from airflow.sensors.filesystem import FileSensor

file_sensor_task = FileSensor(
    task_id="file_sense",
    filepath="salesdata.csv",
    poke_interval=300,
    dag=sales_report_dag,
)

init_sales_cleanup >> file_sensor_task >> generate_report
```

這種 pattern 很適合：

- 檔案到齊後才開始處理
- 防止下游報表 task 太早執行

### Other Sensors

除了 `FileSensor`，教材也提到像 `HttpSensor` 這類型別。

重點不是背所有 sensor 名稱，而是理解 sensor 解決的是「外部條件未滿足時，workflow 要怎麼有紀律地等待」。

## Templates and Jinja

Airflow template 的核心價值是讓 task definition 更動態，而不是為了炫技。

它通常用 Jinja syntax 在 DAG run 時插入值。

### Why Templates Matter

沒有 template 時，很容易寫出重複 task：

```python
t1 = BashOperator(
    task_id="first_task",
    bash_command='echo "Reading file1.txt"',
    dag=dag,
)

t2 = BashOperator(
    task_id="second_task",
    bash_command='echo "Reading file2.txt"',
    dag=dag,
)
```

有 template 後，可以把變動部分抽出來：

```python
templated_command = """
  echo "Reading {{ params.filename }}"
"""

t1 = BashOperator(
    task_id="template_task",
    bash_command=templated_command,
    params={"filename": "file1.txt"},
    dag=example_dag,
)
```

這種做法的優點是：

- task 定義更可重用
- 變動值與執行邏輯分離
- 比大量 copy-paste 任務更好維護

## `default_args`

`default_args` 是 Airflow 裡很常見的共用設定入口。

可以把它理解成：

- 把多個 task 或 DAG 常共用的參數先集中管理
- 減少重複設定

常見會放進去的內容包括：

- `start_date`
- retry 相關設定
- email / alert 相關設定
- SLA 類設定

概念上：

```python
default_args = {
    "start_date": start_date,
    "sla": sla_window,
}

dag = DAG("sla_dag", default_args=default_args)
```

這樣做的好處是 DAG 定義比較一致，也更容易在後續調整共同策略。

## A Practical Airflow Reading Order

如果你是第一次看 Airflow，推薦用這個順序理解：

1. workflow / DAG 是什麼
2. operator 與 task 的關係
3. dependency syntax
4. scheduling 與 `start_date`
5. sensors
6. templates
7. CLI-based debugging

這樣比較不會一開始就陷進 deployment 細節。

## Practical Reminders

- Airflow 比較像 orchestrator，不是 transformation engine 本身。
- task 越小越清楚，但過度切碎也會增加管理成本。
- `schedule_interval` 與 `start_date` 的交互很常是新手最先踩的坑。
- sensor 很有用，但等待邏輯要考慮 worker slot 成本，必要時用 `reschedule`。
- template 能減少重複 DAG code，但不要把過多商業邏輯藏進 Jinja 字串。

## Related Concepts

- [Processing and Pipelines](../../../data-science/data-engineering/processing-and-pipelines.md)
- [ETL](../../../data-science/data-engineering/etl.md)
- [Nextflow](../nextflow/README.md)

[Back to Workflow Engines](../README.md)
