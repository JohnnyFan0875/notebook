[Data Science](../README.md) › [Databases](README.md) › 正規化

# 正規化 (Database Normalization)

正規化讓每個事實只存在一個地方，避免同一資訊散落多處而互相矛盾。目標不是把表拆得越碎越好，而是讓每個欄位都依賴「正確的 key」。Key 的名詞（candidate key、composite key）見 [資料庫設計原則](database-design-principles.md#key)。

## 不正規化會出什麼問題

以一張把所有資訊塞在一起的樣本表為例：

| sample_id | patient_id | patient_sex | assay | assay_vendor | vendor_site |
| --- | --- | --- | --- | --- | --- |
| S1 | P1 | F | RNA-seq | Illumina | illumina.com |
| S2 | P1 | F | WGS | Illumina | illumina.com |
| S3 | P2 | M | RNA-seq | Illumina | illumina.com |

| 異常 | 例子 |
| --- | --- |
| 更新異常 (update anomaly) | P1 的性別登錄錯誤，要改兩列；漏改一列就互相矛盾 |
| 新增異常 (insert anomaly) | 想先登錄一位還沒採檢的病人，卻沒有 `sample_id` 可以填 |
| 刪除異常 (delete anomaly) | 刪掉 S3，P2 的性別資訊也跟著消失 |

## 函數相依 (Functional Dependency)

`A → B` 表示知道 A 就能唯一決定 B。上表中：

- `sample_id → patient_id, assay`
- `patient_id → patient_sex`（性別是病人的屬性，不是樣本的）
- `assay_vendor → vendor_site`

正規化就是讓每個非 key 欄位**只**依賴它所屬實體的 key：「the key, the whole key, and nothing but the key」。

## 1NF、2NF、3NF

| 正規形式 | 要求 | 違反的訊號 | 改法 |
| --- | --- | --- | --- |
| 1NF | 每格是單一值；沒有重複欄組 | 一格塞多值（`"TP53,KRAS"`）；`phone1`、`phone2`、`phone3` | 多值拆成多列或獨立關聯表 |
| 2NF | 1NF + 非 key 欄依賴**整個** key（沒有部分相依） | composite key `(textbook_id, publisher_id)` 中，`publisher_site` 只依賴 `publisher_id` | 把只依賴部分 key 的欄位拆成獨立表 |
| 3NF | 2NF + 非 key 欄不依賴其他非 key 欄（沒有遞移相依） | `employee` 表裡 `department_location` 依賴 `department_name` | 把被依賴的欄位與它決定的欄位拆成獨立表 |
| BCNF | 每個決定因子都是 candidate key | 3NF 仍有少數重疊 candidate key 的異常 | 實務上 3NF 通常已足夠 |

> 2NF 只會在 composite key 上被違反：單欄主鍵的表滿足 1NF 就自動滿足 2NF。

1NF 的多值欄位：

```sql
-- 違反 1NF：mutated_genes = 'TP53,KRAS'，無法用 WHERE / JOIN 直接查單一基因
-- 改成關聯表，一個 (樣本, 基因) 一列
CREATE TABLE sample_mutations (
  sample_id TEXT REFERENCES samples (sample_id),
  gene      TEXT NOT NULL,
  PRIMARY KEY (sample_id, gene)
);
```

2NF：把只依賴 `publisher_id` 的欄位拆出去。

```sql
CREATE TABLE publisher (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  site TEXT
);

CREATE TABLE textbook (
  id           INTEGER PRIMARY KEY,
  name         TEXT NOT NULL,
  quantity     SMALLINT NOT NULL DEFAULT 0,
  publisher_id INTEGER REFERENCES publisher (id)
);
```

把開頭的樣本表正規化到 3NF：

```
patients(patient_id PK, sex)
vendors(vendor PK, site)
assays(assay PK, vendor FK)
samples(sample_id PK, patient_id FK, assay FK)
```

## 反正規化的取捨

| 系統 | 取向 | 原因 |
| --- | --- | --- |
| OLTP（LIMS、EHR） | 正規化到 3NF | 頻繁寫入，一致性優先 |
| 資料倉儲 / BI | 部分反正規化（星狀模型） | 以讀為主，減少 join；由 ETL 負責維持一致 |
| 分析用的資料框 | 一張寬表（tidy data） | 建模與繪圖需要一列一觀測；在 SQL 或 pandas 中 join 好再分析 |

反正規化前先確認：冗餘帶來的維護成本由誰承擔（ETL 會不會重算）、資料是否以讀為主。分析時把正規化的表 join 成寬表是正常流程，不代表資料庫該存成寬表。

## 檢查清單

| 問題 | 疑似違反 |
| --- | --- |
| 一格裡有逗號分隔的多個值？ | 1NF |
| 欄位只依賴 composite key 的一部分？ | 2NF |
| 欄位由另一個非 key 欄位決定（郵遞區號 → 城市）？ | 3NF |
| 同一段文字重複出現很多次？ | 考慮 surrogate key + lookup table |
| 幾個欄位總是一起描述另一個實體？ | 拆成獨立表 |
