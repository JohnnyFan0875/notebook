[Data Science](../README.md) › [Data Engineering](README.md) › 資料品質檢查

# 資料品質檢查 (Data Quality Checks)

資料品質是確保資料「適合預期用途」的持續作業：定義品質維度、寫成可測試的規則、設定閾值與告警、指定誰負責修。本篇是組織與 pipeline 層級的做法；分析前清理單一資料集見 [Statistics：資料品質](../statistics/descriptive-statistics/data-quality.md)，程式內的 assert 見 [錯誤與斷言](../python-foundations/errors-and-assertions.md)。

> 資料品質不只是清掉壞列，而是把業務期待、技術驗證、告警與負責人串起來的作業紀律。來源會變、規則會變、用途會變，所以它是持續的流程。

## 品質維度

| 維度 | 定義 | 一般例子 | 生資例子 |
| --- | --- | --- | --- |
| 完整性 (completeness) | 該有的記錄與欄位都在 | 必填欄位有值 | 每個樣本都有 metadata；計數矩陣沒有整欄缺失 |
| 有效性 (validity) | 值符合格式、範圍、業務條件 | 出生日期在過去；狀態只能是 `Open` / `Closed` | 計數 ≥ 0 且為整數；染色體在允許集合內；Phred 分數範圍 |
| 唯一性 (uniqueness) | 該唯一的不重複 | 客戶 ID 唯一 | 樣本 ID 唯一；同一基因不重複列 |
| 一致性 (consistency) | 跨表、跨系統、跨時間相符 | 帳戶表的客戶 ID 都存在於客戶表；今日筆數在昨日 ±5% | metadata 樣本 ID 集合 = 矩陣欄名集合；登記性別與 X / Y 表現量相符 |
| 及時性 (timeliness) | 在需要時已到位 | 每日資料 9:00 前載入 | 定序結果在 tumor board 前完成 |
| 準確性 (accuracy) | 與現實或可信來源相符 | 地址與報稅資料一致 | 樣本身分與基因型指紋 (SNP fingerprint) 相符 |

完整性可分資料集層級（所有預期記錄都載入）與欄位層級（必填欄位有值）。有效性幾乎都需要業務脈絡：格式正確的值仍可能對流程無效。資料完整、有效但太晚到，對營運仍然沒用。

## 品質規則

規則把「資料要乾淨」這類模糊期待轉成可以測試的條件。

| 維度 | 資料集層級規則 | 欄位層級規則 |
| --- | --- | --- |
| 完整性 | 所有來源記錄都載入目標表 | `sample_id`、`tissue`、`batch` 不可為空 |
| 有效性 | — | `collection_date` 是有效日期且不在未來；`sex` ∈ {F, M, unknown} |
| 唯一性 | — | `sample_id` 唯一 |
| 一致性 | 今日筆數在昨日 ±5% | 結果表的 `sample_id` 都存在於樣本表 |
| 及時性 | 每日資料 9:00 前載入 | 報告送出前 `qc_status` 已填 |
| 準確性 | 通常靠對帳 (reconciliation) | 與可信來源文件比對 |

### 偵測型 vs 預防型規則

| 類型 | 目的 | 行為 | 適合 |
| --- | --- | --- | --- |
| 偵測型 (detective) | 資料載入後監控 | 告警、調查、修正 | 不立即修也不會造成重大傷害、問題複雜難以快速修、影響的記錄少 |
| 預防型 (preventative) | 阻止壞資料往下游流 | 擋下載入直到問題解決 | 資料對流程關鍵、會立即造成傷害、能快速修、影響的記錄多 |

> 剛開始先偵測、累積經驗；等業務影響與修正路徑都清楚後再改成預防。

### 閾值與告警

| 層級 | 意義 | 回應 |
| --- | --- | --- |
| Level 1：警告 | 超過閾值但不需立即修 | 監控、排入清理 |
| Level 2：嚴重告警 | 超過閾值且需快速修正 | 升級處理、盡快修 |
| Level 3：嚴重阻擋 | 超過閾值且不應繼續往下游 | 擋下 pipeline 或發布 |

閾值是失敗筆數或比例的上限，依關鍵程度設定：越關鍵的欄位閾值越嚴。閾值設計同時是業務決策：它決定哪些缺陷可以容忍。

### 異常偵測

規則之外，也可以用異常偵測 (anomaly detection) 監控大量資料：設定成本低、能抓到固定閾值漏掉的分布漂移。但它只找出可疑模式，不能取代關鍵控制的業務規則。

## 角色與修正流程

| 角色 | 責任 |
| --- | --- |
| 資料產生者 (producer) | 實作規則、修正來源或 pipeline 的技術問題 |
| 資料使用者 (consumer) | 提出規則、使用前了解資料是否合用、回報問題 |
| 治理團隊 | 定義政策與角色、監控 dashboard、提供工具與訓練 |

```
使用者發現問題或缺少的規則 → 產生者實作 / 更新規則並修正 → 治理團隊追蹤進度
```

同一個人常在不同步驟同時是 producer 與 consumer，所以每個交接點的負責人要明確。

## 用程式實作：pandera

[pandera](https://pandera.readthedocs.io/) 用 schema 宣告 DataFrame 的欄位型別與檢查，適合分析程式與中小型 pipeline。

```python
import pandas as pd
import pandera.pandas as pa          # 舊版：import pandera as pa

sample_schema = pa.DataFrameSchema(
    {
        "sample_id": pa.Column(str, unique=True, nullable=False),
        "patient_id": pa.Column(str, nullable=False),
        "sex": pa.Column(str, pa.Check.isin(["F", "M", "unknown"])),
        "age": pa.Column(float, pa.Check.in_range(0, 120), nullable=True),
        "batch": pa.Column(str),
        "rin": pa.Column(float, pa.Check.ge(0) & pa.Check.le(10), nullable=True),
    },
    strict=True,             # 不允許多出來的欄位（上游偷改欄名時會報錯）
    coerce=True,             # 先嘗試轉型
)

meta = sample_schema.validate(meta, lazy=True)   # lazy=True：收集所有錯誤一次回報
```

## 生資資料的一致性檢查

型別與範圍之外，最常出事的是表與表之間對不上：

```python
import numpy as np

counts = pd.read_parquet("counts.parquet")       # genes × samples
meta = pd.read_csv("samples.tsv", sep="\t", dtype={"sample_id": "string"})

# 1. 樣本對齊：集合相同，而且順序一致（很多工具依位置對應）
missing_in_meta = set(counts.columns) - set(meta["sample_id"])
missing_in_counts = set(meta["sample_id"]) - set(counts.columns)
assert not missing_in_meta and not missing_in_counts, (missing_in_meta, missing_in_counts)
meta = meta.set_index("sample_id").loc[counts.columns]

# 2. 計數矩陣本身
assert counts.index.is_unique                        # 基因不重複
assert (counts.values >= 0).all()                    # 無負值
assert np.allclose(counts.values, counts.values.round())   # 原始計數應為整數（TPM 不是）
lib_size = counts.sum()
assert (lib_size > 1e6).all(), lib_size[lib_size <= 1e6]   # 定序深度門檻依實驗設定

# 3. 跨資料的準確性：登記性別 vs XIST / Y 染色體基因表現
```

| 檢查 | 抓到的問題 |
| --- | --- |
| metadata ↔ 矩陣樣本 ID | 樣本漏掉、命名不一致、多一個 Undetermined |
| 欄位順序對齊 | 標籤錯位（最危險：不會報錯、結果全錯） |
| 基因 ID 格式一致 | 有些帶版本號 `.17`、有些是 symbol |
| 性別 vs 性染色體表現 | 樣本調換 (sample swap) |
| SNP fingerprint | 同一病人的 tumor / normal 是否真的同一人 |
| 批次 × 組別交叉表 | 批次與實驗組完全混淆（無法分開效應） |

更多 omics QC 見 [EDA](../data-manipulation-and-eda/README.md)；批次效應見 [Statistics](../statistics/README.md)。

## 用程式實作：Great Expectations

Great Expectations（GX）把品質規則寫成 expectation，對每批新資料重複驗證，並產生給非工程人員看的 Data Docs。適合同一份資料要反覆驗證、規則要在團隊間共享、失敗要觸發告警的情況；一次性探索清理則不必用。

| 概念 | 意義 |
| --- | --- |
| Data Context | GX 的入口，管理設定與元件 |
| Data Source / Data Asset / Batch Definition | 資料從哪來、哪一份、如何切成批次 |
| Expectation | 一條可驗證的斷言 |
| Expectation Suite | 一組 expectation，對應一份資料或一個用途 |
| Validation Definition | 把 batch 與 suite 綁在一起 |
| Checkpoint | 執行一或多個 validation 並觸發後續動作（通知、更新文件） |
| Data Docs | 人可讀的 suite 與驗證結果 |

```python
import great_expectations as gx      # GX Core 1.x 的 API；0.x 版差異很大

context = gx.get_context()
batch_def = (context.data_sources.add_pandas("pandas")
             .add_dataframe_asset("samples")
             .add_batch_definition_whole_dataframe("all"))

suite = context.suites.add(gx.ExpectationSuite(name="samples_critical"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="sample_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="sample_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(column="sex", value_set=["F", "M", "unknown"]))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="rin", min_value=0, max_value=10))

vd = context.validation_definitions.add(
    gx.ValidationDefinition(name="samples_vd", data=batch_def, suite=suite))
result = vd.run(batch_parameters={"dataframe": meta})
result.success                         # False 時擋下 pipeline 或告警
```

| Expectation 類型 | 例子 | 對應維度 |
| --- | --- | --- |
| 逐列 | `ExpectColumnValuesToNotBeNull`、`ExpectColumnValuesToBeOfType`、`ExpectColumnValuesToBeBetween`、`ExpectColumnValuesToMatchRegex` | 完整性、有效性 |
| 聚合 | `ExpectColumnDistinctValuesToEqualSet`、`ExpectColumnUniqueValueCountToBeBetween`、`ExpectColumnMostCommonValueToBeInSet` | 一致性 |
| 唯一性 | `ExpectColumnValuesToBeUnique`、`ExpectCompoundColumnsToBeUnique` | 唯一性 |
| 及時性 / 準確性 | 通常在 GX 之外處理，或寫自訂 expectation 比對參考資料 | — |

suite 要聚焦：一個 suite 描述一份穩定的品質契約（例如「阻擋型關鍵檢查」與「建議型檢查」分開），而不是收集所有可能的檢查。

## 工具選擇

| 工具 | 語言 | 適合 |
| --- | --- | --- |
| `assert` / 自寫檢查函式 | Python / R | 分析腳本、少量關鍵條件 |
| pandera | Python（pandas、Polars、PySpark） | 以 schema 宣告型別與檢查，輕量 |
| Great Expectations | Python | 團隊共享規則、驗證歷史、Data Docs |
| dbt tests | SQL | warehouse 內的表，見 [dbt 測試](dbt-foundations.md#測試) |
| `pointblank`、`validate` | R | R 的資料驗證與報告 |

## 健全的品質作業應該說得出

1. 這份資料重要的品質維度是哪些、為什麼
2. 執行了哪些資料集層級與欄位層級的規則
3. 什麼時候只偵測、什麼時候阻擋下游
4. 閾值與告警依關鍵程度怎麼設定
5. 誰負責修正、升級與監控
