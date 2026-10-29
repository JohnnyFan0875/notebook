[Data Science](../README.md) › [Data Engineering](README.md) › 資料建模基礎

# 資料建模基礎 (Data Modeling Foundations)

資料建模先把世界拆成實體、屬性與關係，再決定落成哪些表、用哪些 key 串起來。建模做得好，後續 join、權限、品質檢查與分析模型都會更穩；沒做好，常見的結果是同一概念存在多處、join key 格式不一致、分析表查得出數字但語意已經偏掉。

## 三個基本元素

| 元素 | 意義 | 一般例子 | 生資例子 |
| --- | --- | --- | --- |
| 實體 (entity) | 可獨立辨識的對象 | customer、order、product | patient、sample、sequencing run、gene |
| 屬性 (attribute) | 實體的描述欄位 | 姓名、下單日期 | 性別、組織類型、read length、gene symbol |
| 關係 (relationship) | 實體之間的連結 | customer places order | patient 提供多個 sample；sample 在多個 run 中定序 |

## 關係基數 (Cardinality)

| 類型 | 例子 | 表的設計 |
| --- | --- | --- |
| 一對一 (1:1) | patient ↔ 去識別化代碼 | 合併成一張表，或任一側放外鍵 |
| 一對多 (1:N) | patient → samples | 外鍵放在「多」的那側（`sample.patient_id`） |
| 多對多 (M:N) | samples ↔ runs（一個樣本多次定序、一個 run 含多個樣本） | 需要 bridge / junction table（`sample_run(sample_id, run_id, lane)`） |

基數決定外鍵放哪裡、需不需要 bridge table，也決定 join 後列數會不會意外膨脹，見 [JOIN 列數膨脹](../databases/sql-joins-and-set-operations.md#列數膨脹-fan-out)。

> 把多對多硬塞進單一欄位（`runs = "R1;R2;R3"`）之後查詢與清理都很痛，應該拆成 bridge table。

## 主鍵與外鍵 (Primary / Foreign Key)

| | 主鍵 (primary key) | 外鍵 (foreign key) |
| --- | --- | --- |
| 作用 | 唯一識別一筆資料 | 指向另一張表的主鍵，表達關係 |
| 條件 | 唯一、非空、穩定 | 值必須存在於被參照的表（參照完整性） |

| 主鍵類型 | 來源 | 優點 | 缺點 |
| --- | --- | --- | --- |
| 自然鍵 (natural key) | 業務系統，如病歷號、Ensembl ID | 有意義、可直接對外 | 可能變動或重用（基因改名、ID 改版） |
| 代理鍵 (surrogate key) | 系統產生的流水號或 UUID | 穩定、單欄、與業務規則解耦 | 本身沒有意義，需要另外保存自然鍵 |

```
patient (patient_id PK, sex, birth_year)
   │ 1:N
sample  (sample_id PK, patient_id FK, tissue, collection_date)
   │ M:N  ── sample_run (sample_id FK, run_id FK, lane)  ── run (run_id PK, platform, run_date)
   │ 1:N
assay_result (sample_id FK, gene_id FK, value)  ── gene (gene_id PK, symbol, biotype)
```

> 基因用 Ensembl stable ID（`ENSG...`）當 key，symbol 只當屬性：symbol 會改名（`SEPT2` → `SEPTIN2`），也有一對多的情況。

## 正規化 (Normalization)

正規化讓同一個事實只存一次，更新不會牽動很多列，刪一筆資料也不會順手刪掉其他資訊。交易型與上游整合型的設計通常會正規化；分析型模型則常在可接受的範圍內反正規化以換取查詢方便。1NF–3NF、函數相依與更新異常的完整說明見 [正規化](../databases/database-normalization.md)。

## ER Model 與分析模型

| 模型 | 目標 | 位置 |
| --- | --- | --- |
| ER / 正規化關聯模型 | 一致性、去重、易維護 | 上游：整合來源、記錄事實 |
| 維度模型 (star schema) | 查詢易懂、彙總快 | 下游：給 BI、分析、feature table |

ER model 介於業務理解與實體表之間：先用 entity 與 relationship 把概念講清楚，在真正建表前檢查 cardinality 與 key 是否合理。很多平台會在上游整理好實體與關係，再於下游轉成 [維度模型](dimensional-modeling-and-star-schema.md)。

## 建模前的檢查清單

| 問題 | 為什麼重要 |
| --- | --- |
| 每張表一列代表什麼（grain）？ | grain 不清楚，聚合必錯 |
| 每個實體的 key 是什麼？會不會變？ | 決定 join 是否穩定 |
| 哪些是多對多關係？ | 需要 bridge table |
| key 的格式在各來源一致嗎？（大小寫、前導零、版本號後綴 `ENSG00000141510.17` vs `ENSG00000141510`） | 格式不一致會讓 join 默默掉資料 |
| 需要保留歷史嗎？ | 決定 SCD 策略，見 [緩慢變化維度](dimensional-modeling-and-star-schema.md#緩慢變化維度-scd) |
