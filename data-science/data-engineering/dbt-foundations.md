# dbt Foundations

dbt 是一個把資料轉換工作工程化的工具。它的重點不是把資料從外部系統「搬進來」，而是把已經在 database 或 warehouse 裡的資料，用 SQL 或 Python 模型整理成可重用、可測試、可追蹤的分析資料資產。

## What dbt Does

- 把轉換邏輯拆成可版本控制的 model 檔案
- 讓資料轉換以 dependency graph 的方式組織，而不是一堆獨立 SQL
- 把 testing、documentation 與 lineage 一起放進同一個 workflow
- 常見用法是把 raw / staging 資料一步步整理成 analytics-ready tables or views

## Mental Model

- dbt project: 一個完整的轉換專案，包含設定、models、文件與 tests
- model: 一個轉換單元，通常是一個 `.sql` 檔，內容多半是 `SELECT` 查詢
- materialization: model 要被建成什麼實體，例如 `view` 或 `table`
- profile: dbt 連到哪個 execution target，例如 dev、staging、prod

## Project Workflow

一個基本的 dbt workflow 可以整理成：

1. 用 `dbt init` 建立 project
2. 在 `profiles.yml` 定義執行環境與連線方式
3. 在 `models/` 下建立轉換模型
4. 用 `dbt run` materialize models
5. 用 testing、docs 與 troubleshooting 驗證結果
6. 持續迭代 models 與設定

## Project Structure

dbt project 通常會包含：

- `dbt_project.yml`: 專案層級設定檔，每個 project 一份
- `models/`: SQL 或 Python models
- `schema.yml` 或其他 `.yml` 檔: model、column、test、source 的描述
- `target/`: build artifacts 與產出資訊

可以把它理解成「資料轉換專案的程式碼目錄」，而不是只存一份 SQL 腳本。

## Creating a Project

```bash
dbt init my_project
```

`dbt init` 會：

- 建立 top-level project folder
- 建立基本目錄結構
- 詢問 project 名稱
- 詢問要使用的 database / warehouse 類型

## Profiles and Environments

`profiles.yml` 用來定義執行環境。

常見 target 包括：

- `dev`
- `staging`
- `prod`

簡化範例：

```yaml
my_project:
  outputs:
    dev:
      type: duckdb
      path: dbt.duckdb
    prod:
      type: snowflake
      ...
  target: dev
```

重點不是 YAML 細節本身，而是：

- 同一個 project 可以對應多個 deployment scenario
- model code 可以不變，但 target warehouse 或 credentials 可以切換
- 這讓本地開發、測試與正式環境能被同一套 project 管理

## Models

### What a dbt Model Is

- model 代表一段轉換邏輯
- 通常寫成 SQL
- 新版本也可以支援 Python model
- 最常見型態是一個 `SELECT` 查詢

簡化範例：

```sql
select
  first_name,
  last_name,
  shipping_address,
  item_quantity
from source_table
```

建立方式通常是：

```bash
mkdir -p models/order
touch models/order/customer_orders.sql
dbt run
```

### Materialization

`dbt run` 會把 model materialize 成 warehouse 內的物件。

最常見的是：

- `view`: 不直接儲存資料內容，查詢時再即時展開
- `table`: 會把結果實際寫入 database / warehouse

粗略地說：

- `view` 比較輕量，適合邏輯清楚、即時查詢可接受的情境
- `table` 比較像轉換後的實體結果，適合重用頻繁或成本高的查詢

## Running Models

```bash
dbt run
```

使用情境：

- model 內容改變後重新執行
- 需要把轉換結果重新 materialize 時

`dbt run` 的輸出通常會顯示：

- dbt version
- 哪些 model 被執行
- 每一步成功或失敗狀態
- 總結是否完成

## Jinja and ref()

dbt 不是只把 SQL 原封不動送出去，它也會透過 Jinja template language 來建立可重用邏輯。

最重要的例子之一是 `ref()`：

```sql
select *
from {{ ref('taxi_rides_raw') }}
```

`ref()` 的價值在於：

- 建立 model 之間的依賴關係
- 讓 dbt 自動推導 lineage / DAG
- 避免把上游資料表名稱硬寫死在每份 SQL

## Documentation and Lineage

dbt 很適合把 documentation 跟 transformation code 放在一起維護。

它可以記錄：

- model description
- column description
- tests / validations
- lineage / DAG
- warehouse metadata，例如欄位型別

簡化範例：

```yaml
version: 2

models:
  - name: taxi_rides_raw
    description: Yellow Taxi raw data
    access: public
  - name: avg_fare_per_day
    description: Average ride per day
    access: public
```

常見指令：

```bash
dbt docs generate
dbt docs serve
```

通常會先跑完 `dbt run`，再產生 docs。

## Testing in dbt

dbt 的一個重要價值，是把資料驗證變成 project 內可版本控制的規則，而不是只靠人工 spot check。

從心智模型上看，test 就是在對 dbt objects 做 assertions，例如：

- 欄位不應該是 null
- 某欄位值只能落在特定集合
- 某欄位必須和另一張表保持關聯
- 某個商業條件不能被違反

這些測試不只可以套在 models，也可以套在 sources 和 seeds。

### Built-in Tests

課程裡最值得留下來的 built-in tests 有四種：

- `unique`
- `not_null`
- `accepted_values`
- `relationships`

簡化範例：

```yaml
version: 2

models:
  - name: taxi_rides_raw
    columns:
      - name: tpep_pickup_datetime
        tests:
          - not_null
      - name: payment_type
        tests:
          - not_null
          - accepted_values:
              values: [1, 2, 3, 4, 5, 6]
```

這些測試通常定義在 `schema.yml` 或其他放在 `models/` 下的 `.yml` 檔案中。

### Running and Debugging Tests

常見指令：

```bash
dbt test
dbt test --select model_name
```

如果測試失敗，一個很實用的排錯方式是：

1. 找到 dbt 編譯後的 SQL。
2. 找出對應失敗 test 的 `.sql`。
3. 把查詢貼回資料庫 client 直接看失敗資料列。
4. 修正資料或邏輯後，再重新跑 `dbt run` / `dbt test`。

這個流程很重要，因為 dbt test 本質上就是 SQL；理解它最後展開成什麼查詢，會比只看錯誤訊息更有效。

### Singular Tests

`singular test` 是自訂的單一測試查詢，通常放在 `tests/` 目錄下，重點是：

- 用 SQL 寫
- 回傳的是「失敗資料列」
- 只要有 rows 回來，test 就失敗

例如驗證 `order_total >= subtotal`：

```sql
select *
from {{ ref('order') }}
where order_total < subtotal
```

這類測試很適合放商業規則、跨欄位條件，或 built-in tests 不夠表達的資料品質限制。

### Generic Tests

如果一個測試邏輯會被多個 models / columns 重用，就更適合寫成 generic test。

generic test 通常：

- 用 Jinja 包成 `{% test ... %}` 區塊
- 存在 `tests/generic/` 下
- 再於 `.yml` 檔內像 built-in test 一樣引用

簡化範例：

```sql
{% test check_gt_0(model, column_name) %}
select *
from {{ model }}
where {{ column_name }} <= 0
{% endtest %}
```

套用時：

```yaml
version: 2

models:
  - name: taxi_rides_raw
    columns:
      - name: total_fare
        tests:
          - check_gt_0
```

如果測試需要額外參數，也可以像 `accepted_values` 一樣傳入：

```yaml
models:
  - name: order
    columns:
      - name: order_time
        tests:
          - check_columns_unequal:
              column_name2: shipped_time
```

## Sources

`source` 用來描述由 EL / ingestion 流程載入 warehouse 的原始資料。

它的重要性不只是在引用方便，而是它能把 raw data 的 lineage、documentation 與 tests 一起納入 dbt project。

### Why Use Sources

- 讓 raw tables 有明確名稱與描述
- 讓 downstream models 不必把原始表名硬寫死
- 讓 lineage 從 raw layer 就開始清楚可追
- 讓 sources 也能被測試與文件化

### Defining Sources

通常在 `.yml` 檔內使用 `sources:` 區塊：

```yaml
version: 2

sources:
  - name: raw
    tables:
      - name: phone_orders
      - name: web_orders
```

在 model 中則用：

```sql
select *
from {{ source('raw', 'orders') }}
```

可以把它理解成：`ref()` 用來連接 dbt models，`source()` 用來連接 project 外部已存在的上游資料。

### Testing Sources

sources 也可以像 models 一樣在 `.yml` 中定義 tests。

這很有用，因為很多資料品質問題其實發生在 raw layer。如果只驗證下游 models，問題常常已經被放大或掩蓋。

## Seeds

`seed` 是放進 project 的靜態 CSV 資料，dbt 可以直接把它匯入 warehouse。

它比較適合：

- 小型對照表
- mapping tables
- demo / bootstrap data
- 不常變動的 reference data

### How Seeds Work

- 把 CSV 放進 `seeds/` 目錄
- 用 `dbt seed` 匯入
- 之後就能像其他 relation 一樣被下游引用

```bash
dbt seed
```

seeds 也可以用 `.yml` 補 description、tests 與其他設定，心智模型上和 models / sources 類似。

### When Seeds Are a Good Fit

seed 適合小而穩定的靜態資料，但如果資料量大、更新頻繁，或需要持續 ingest，通常就不該再用 seed，而應該改走正式的 ingestion pipeline。

## Snapshots

snapshot 是 dbt 用來追蹤資料隨時間變化的機制，常被拿來做類似 `SCD Type 2` 的歷史保留。

當你想回答這類問題時，snapshot 很有用：

- 某筆 customer 資料以前長什麼樣子
- 某個狀態是什麼時候改變的
- 當前值之外，是否需要保留歷史版本

### Snapshot Mental Model

可以把 snapshot 理解成：

- source / model 提供目前狀態
- snapshot 負責把狀態變更保留下來
- 下游查詢可以再透過 `ref()` 去讀 snapshot 結果

簡化範例：

```sql
{% snapshot snapshot_orders %}
  {{
    config(
      target_schema='snapshots'
    )
  }}

  select *
  from {{ source('raw', 'orders') }}
{% endsnapshot %}
```

常見操作：

```bash
dbt snapshot
```

之後可以在 model 裡查：

```sql
select *
from {{ ref('snapshot_orders') }}
```

### When to Use Snapshots

如果你只需要最新狀態，snapshot 可能太重；但如果分析需要歷史追蹤，或來源系統本身不保留版本，snapshot 會很有價值。

## Why dbt Matters in Data Engineering

dbt 的價值不只是「可以跑 SQL」，而是把資料轉換帶進比較像軟體工程的工作方式：

- project structure 明確
- 轉換邏輯可版本控制
- environment 可切換
- model 依賴可追蹤
- documentation、testing、lineage 可以跟 code 一起演進
- sources、seeds 與 snapshots 讓上游資料、靜態參照資料與歷史追蹤能被收斂進同一套 workflow

對 data team 來說，這通常比單純把 SQL 散落在 BI tool、notebook 或 warehouse query history 裡更可維護。
