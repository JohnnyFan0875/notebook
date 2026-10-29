[臨床資訊與標準](../README.md) › [臨床資料庫](README.md) › MIMIC-IV

# MIMIC-IV

MIMIC-IV 是 Beth Israel Deaconess Medical Center (BIDMC) 急診與 ICU 病人的去識別化病歷，是臨床資料研究與醫療 ML 最常用的公開資料庫之一。

| 項目 | 內容 |
| --- | --- |
| 網站 | [physionet.org/content/mimiciv](https://physionet.org/content/mimiciv/)、文件 [mimic.mit.edu](https://mimic.mit.edu) |
| 版本 | v3.1（2024-10） |
| 範圍 | 2008–2022 年入急診或 ICU 的病人；v3.0 約 36.5 萬病人、54.6 萬次住院、9.4 萬次 ICU 住院 |
| 申請 | PhysioNet credentialing + CITI 訓練 + 簽 DUA，見 [PhysioNet](physionet.md) |
| 存取 | 下載 CSV、或 BigQuery（`mimiciv_v3_1_hosp`、`mimiciv_v3_1_icu`） |
| 程式碼 | [mimic-code](https://github.com/MIT-LCP/mimic-code)（官方建庫腳本與衍生概念，如 SOFA、sepsis-3） |

## 模組

| 模組 | 內容 | 主要資料表 |
| --- | --- | --- |
| `hosp` | 全院層級 EHR | `patients`、`admissions`、`transfers`、`labevents`、`prescriptions`、`diagnoses_icd`、`procedures_icd`、`microbiologyevents` |
| `icu` | ICU 臨床資訊系統（MetaVision） | `icustays`、`chartevents`、`inputevents`、`outputevents`、`procedureevents`、`d_items` |
| 相關獨立資料集 | 急診 MIMIC-IV-ED、病歷文字 MIMIC-IV-Note、MIMIC-IV-ECG、胸部 X 光 MIMIC-CXR | 各自申請 |

```sql
-- 成人第一次 ICU 住院 + 入 ICU 首日的肌酸酐最大值
WITH first_icu AS (
  SELECT i.subject_id, i.hadm_id, i.stay_id, i.intime,
         ROW_NUMBER() OVER (PARTITION BY i.subject_id ORDER BY i.intime) AS rn
  FROM mimiciv_icu.icustays i
)
SELECT f.stay_id, p.anchor_age, MAX(l.valuenum) AS creat_max_d1
FROM first_icu f
JOIN mimiciv_hosp.patients p USING (subject_id)
LEFT JOIN mimiciv_hosp.labevents l
  ON l.subject_id = f.subject_id
 AND l.itemid = 50912                                  -- Creatinine（查 d_labitems）
 AND l.charttime BETWEEN f.intime AND f.intime + INTERVAL '1 day'
WHERE f.rn = 1 AND p.anchor_age >= 18
GROUP BY f.stay_id, p.anchor_age;
```

視窗函數的用法見 [SQL 視窗函數](../../../data-science/databases/sql-window-functions.md)。

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 日期位移 | 每位病人的日期平移到 2100–2200 年，只能算同一病人內的時間差；真實年代看 `anchor_year_group` |
| 年齡 | 用 `anchor_age`（在 `anchor_year` 時的年齡）推算；89 歲以上被歸為同一值 |
| ICD 版本混用 | `diagnoses_icd` 同時有 ICD-9 與 ICD-10（看 `icd_version`），定義疾病要兩版都列，見 [ICD](../clinical-terminology/icd.md) |
| 代碼 | 檢驗與 ICU 項目用 `itemid`，需查 `d_labitems` / `d_items`；同一概念可能有多個 `itemid` |
| `chartevents` 很大 | 數億列；先用 `itemid` 與 `stay_id` 過濾，或用 BigQuery / DuckDB 處理，見 [DuckDB 與 Parquet](../../../data-science/databases/duckdb-and-parquet.md) |
| 單一中心 | 結果需在其他資料（如 [eICU](eicu.md)）外部驗證 |
