[臨床資訊與標準](../README.md) › [臨床術語](README.md) › UCUM

# UCUM

UCUM (Unified Code for Units of Measure) 是計量單位的機器可讀寫法。檢驗值的單位在不同系統常寫成 `mg/dl`、`mg/dL`、`mg%`，UCUM 規定唯一的正式寫法，並能把單位拆解成基本單位，讓程式能檢查兩個單位是否可互換。

| 項目 | 內容 |
| --- | --- |
| 維護 | Regenstrief Institute（與 LOINC 同單位） |
| 網站 | [ucum.org](https://ucum.org)（規格、線上驗證工具） |
| 授權 | 免費 |
| 何時用 | FHIR `Quantity`（`system = http://unitsofmeasure.org`）、OMOP `unit_concept_id`、LOINC 範例單位 |

## 語法規則

| 規則 | 例 | 說明 |
| --- | --- | --- |
| 大小寫敏感 | `mm`（毫米）vs `Mm`（百萬米）；莫耳濃度寫 `mol/L`，不寫 `M` | 也有大小寫不敏感的變體，但交換時用敏感版 |
| 乘號用 `.` | `kg.m/s2` | 指數直接接在後面（`s2` = s²） |
| 10 的次方用 `10*n` | `10*3/uL` | 白血球「千 / 微升」 |
| 特殊單位用方括號 | `[iU]`、`[in_i]`、`mm[Hg]` | 國際單位、英寸、毫米汞柱 |
| 大括號是註解 | `{cells}/uL`、`{score}` | 不影響換算，等同 1 |
| 溫度 | `Cel`、`[degF]` | 攝氏寫 `Cel` 不是 `°C` |
| 微 | `u` | `ug`、`uL`（不用 µ） |

## 常見檢驗單位

| UCUM | 意義 | 常見檢驗 |
| --- | --- | --- |
| `mg/dL` | 毫克 / 分升 | 血糖、膽固醇、肌酸酐 |
| `mmol/L` | 毫莫耳 / 升 | 血糖（SI）、電解質 |
| `g/dL` | 克 / 分升 | 血紅素、白蛋白 |
| `10*3/uL` | 千 / 微升 | 白血球、血小板 |
| `[iU]/L` / `U/L` | 國際單位 / 升 | 酵素（ALT、AST） |
| `%` | 百分比 | HbA1c（NGSP） |

> UCUM 只能換算**同一量綱**的單位（`mg/dL` ↔ `g/L`）。`mg/dL` ↔ `mmol/L` 需要分子量（血糖 ÷ 18.016），不同物質不同，必須依 LOINC 的 Component 決定，不能只靠 UCUM。
