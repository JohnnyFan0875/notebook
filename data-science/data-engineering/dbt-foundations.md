[Data Science](../README.md) › [Data Engineering](README.md) › dbt

# dbt (data build tool)

dbt 把 warehouse 內的資料轉換工程化：每個轉換寫成一個 SQL（或 Python）model 檔，dbt 依 `ref()` 推出依賴圖、依序在 warehouse 中建成 view 或 table，並把測試、文件與 lineage 放進同一個版本控制的專案。它負責 ELT 的 **T**，不負責把資料從外部搬進來。

| 散落的 SQL（BI 工具、notebook、查詢歷史） | dbt 專案 |
| --- | --- |
| 表名寫死，順序靠人記 | `ref()` 自動推出依賴與執行順序 |
| 品質靠人工 spot check | 測試與 model 一起版本控制 |
| 不知道表怎麼來的 | 自動產生文件與 lineage 圖 |
| dev / prod 各一份 SQL | 同一份程式，切換 target |

## 專案結構

```
my_project/
├── dbt_project.yml       # 專案設定（每專案一份）
├── models/
│   ├── staging/          # 對 source 做輕度清理：改名、轉型
│   │   ├── stg_samples.sql
│   │   └── _sources.yml
│   └── marts/            # 給分析的表
│       ├── fct_results.sql
│       └── _models.yml   # model / 欄位描述與測試
├── seeds/                # 小型靜態 CSV
├── snapshots/            # 歷史追蹤
├── tests/                # singular tests；tests/generic/ 放自訂 generic tests
└── target/               # 編譯後的 SQL 與 artifacts（不進版本控制）
```

| 概念 | 意義 |
| --- | --- |
| Model | 一個轉換單元，通常是一個只含 `SELECT` 的 `.sql` 檔 |
| Materialization | model 建成什麼：`view`、`table`、`incremental`、`ephemeral` |
| Source | 由擷取流程載入的原始表 |
| Profile / target | 連到哪個 warehouse、哪個環境（dev / prod） |

## 建立與設定

```bash
pip install dbt-core dbt-duckdb        # adapter 依 warehouse 選：dbt-snowflake、dbt-bigquery、dbt-postgres...
dbt init my_project                    # 建立目錄並詢問 warehouse 類型
dbt debug                              # 檢查連線
```

```yaml
# ~/.dbt/profiles.yml：同一專案對應多個環境，model 程式碼不變
my_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"   # 帳密放環境變數，不寫進檔案
      database: analytics
      warehouse: transform_wh
      schema: marts
```

## Model 與 `ref()` / `source()`

```yaml
# models/staging/_sources.yml
version: 2
sources:
  - name: raw
    schema: raw
    tables:
      - name: samples
      - name: lab_results
```

```sql
-- models/staging/stg_samples.sql
select
    cast(sample_id as varchar)        as sample_id,
    upper(trim(tissue))               as tissue,
    cast(collection_date as date)     as collection_date
from {{ source('raw', 'samples') }}

-- models/marts/fct_results.sql
{{ config(materialized='table') }}
select r.sample_id, s.tissue, r.test_code, r.value
from {{ source('raw', 'lab_results') }} r
join {{ ref('stg_samples') }} s using (sample_id)
```

| 函式 | 連到 | 作用 |
| --- | --- | --- |
| `ref('model')` | 另一個 dbt model | 建立依賴與 lineage；依環境自動換成正確的 schema |
| `source('src', 'table')` | 專案外已存在的原始表 | 讓 lineage 從 raw 開始；source 也能測試與文件化 |

dbt 用 Jinja 樣板語言編譯 SQL，所以也能寫迴圈、條件與 macro。

| Materialization | 行為 | 適合 |
| --- | --- | --- |
| `view` | 不存資料，查詢時展開 | 輕量、邏輯簡單的中間層 |
| `table` | 每次 `dbt run` 重建整張表 | 常被查、計算成本高 |
| `incremental` | 只處理新資料（`is_incremental()` 判斷） | 大型事實表 |
| `ephemeral` | 不建物件，以 CTE 嵌入下游 | 只被少數 model 使用的小轉換 |

## 常用指令

| 指令 | 作用 |
| --- | --- |
| `dbt run` | 建立 / 更新 models |
| `dbt test` | 執行測試 |
| `dbt build` | 依依賴順序執行 run + test + seed + snapshot（上游測試失敗時跳過下游） |
| `dbt run --select stg_samples+` | 只跑某 model 與其下游（`+model` 為上游） |
| `dbt seed` | 載入 `seeds/` 的 CSV |
| `dbt snapshot` | 執行 snapshots |
| `dbt docs generate && dbt docs serve` | 產生並瀏覽文件與 lineage 圖 |
| `dbt compile` | 只編譯，看 `target/compiled/` 中實際送出的 SQL |

## 測試

dbt 的測試是對資料的斷言，本質上是一段 SQL：**回傳失敗的列，有任何列就代表測試失敗**。可以套在 models、sources、seeds 上。

### 內建 generic tests

```yaml
# models/marts/_models.yml
version: 2
models:
  - name: fct_results
    description: 每個樣本 × 檢驗項目一列
    columns:
      - name: sample_id
        data_tests:                    # dbt 1.8 起的名稱；舊版寫 tests:
          - not_null
          - relationships:
              to: ref('stg_samples')
              field: sample_id
      - name: test_code
        data_tests:
          - accepted_values:
              values: ['GLU', 'HBA1C', 'LDL']
      - name: value
        data_tests:
          - check_gt_0                 # 自訂 generic test，見下
```

| 測試 | 檢查 |
| --- | --- |
| `unique` | 欄位值不重複 |
| `not_null` | 欄位無缺值 |
| `accepted_values` | 值落在指定集合 |
| `relationships` | 值都存在於另一張表（參照完整性） |

### Singular 與自訂 generic tests

```sql
-- tests/assert_order_total_ge_subtotal.sql：singular test，只用一次的業務規則
select * from {{ ref('orders') }}
where order_total < subtotal

-- tests/generic/check_gt_0.sql：generic test，可在 yml 中重複套用
{% test check_gt_0(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
```

generic test 也可以接參數，例如 `check_columns_unequal: {column_name2: shipped_time}`，在 `{% test check_columns_unequal(model, column_name, column_name2) %}` 中使用。

### 測試失敗時

1. 執行 `dbt test --select fct_results` 縮小範圍
2. 到 `target/compiled/` 找到該測試編譯後的 SQL
3. 貼到資料庫 client 直接看失敗的列
4. 修正資料或邏輯後重跑 `dbt build`

> 只驗證下游 model 時，raw 層的問題常已被放大或掩蓋；在 source 上也要放測試。dbt 1.8 起另有 unit tests，用固定的輸入列驗證 model 的 SQL 邏輯。

## Seed

seed 是放在 `seeds/` 的小型靜態 CSV，`dbt seed` 匯入後可以像其他表一樣被 `ref()`。適合對照表、mapping（例如檢驗代碼 ↔ 名稱、樣本 ↔ 批次）、不常變的參考資料。資料量大、常更新或需要持續擷取時，就該改走正式的擷取 pipeline。

## Snapshot

snapshot 追蹤可變資料隨時間的變化，產生 [SCD Type 2](dimensional-modeling-and-star-schema.md#緩慢變化維度-scd) 風格的歷史表（`dbt_valid_from`、`dbt_valid_to`）。適合回答「某筆資料以前長什麼樣」「狀態何時改變」，尤其是來源系統本身不保留版本時；只需要最新狀態就不必用。

```sql
-- snapshots/patients_snapshot.sql
{% snapshot patients_snapshot %}
{{ config(
    target_schema='snapshots',
    unique_key='patient_id',
    strategy='timestamp',          -- 以 updated_at 判斷變更；沒有可靠時間欄時用 strategy='check', check_cols=[...]
    updated_at='updated_at'
) }}
select * from {{ source('raw', 'patients') }}
{% endsnapshot %}
```

`dbt snapshot` 要定期執行（每次執行時比對變更）；下游以 `ref('patients_snapshot')` 讀取。較新版本也可以在 YAML 中設定 snapshot。

## 文件

```yaml
models:
  - name: fct_results
    description: 每個樣本 × 檢驗項目一列；只含通過 QC 的樣本
    columns:
      - name: value
        description: 檢驗值，單位見 test_code 對照表
```

`dbt docs generate` 會結合這些描述、warehouse 的欄位型別與依賴圖，`dbt docs serve` 在瀏覽器中檢視 lineage。
