[臨床資訊與標準](../README.md) › [臨床術語](README.md) › ICD

# 國際疾病分類 (ICD)

國際疾病分類 (International Classification of Diseases, ICD) 是 WHO 維護的疾病、症狀與死因分類，用於死因統計、流行病學與保險申報。病歷資料庫中最常見的診斷代碼就是 ICD，但它是**分類**而不是細緻的臨床語意，定義表型時要注意這點。

| 項目 | 內容 |
| --- | --- |
| 維護 | 世界衛生組織 (WHO) |
| 網站 | [icd.who.int](https://icd.who.int)（ICD-11 瀏覽器、API、Coding Tool） |
| 版本 | ICD-10：1990 年 WHA 通過、1993 年生效；ICD-11：2019 年通過、2022-01-01 生效，每年發布更新版 |
| 授權 | 免費 |

## ICD-10 與 ICD-11

| 項目 | ICD-10 | ICD-11 |
| --- | --- | --- |
| 代碼格式 | 1 字母 + 2 位數字，小數點後可再細分 | 4–6 碼英數混合，第 2 碼必為字母 |
| 例：第 2 型糖尿病 | `E11`（`E11.9` 無併發症） | `5A11` |
| 結構 | 單一階層的章節分類 | 底層是語意網路 (Foundation)，統計用的線性化 (MMS) 從中產生 |
| 組合編碼 | 有限 | stem code + extension code 以 `&` / `/` 組合（如部位、嚴重度） |
| 數位化 | 以書本 / 表格為主 | 原生支援 API 與 Coding Tool |

```
E11   Type 2 diabetes mellitus
 ├── E11.2  With kidney complications
 ├── E11.3  With ophthalmic complications
 └── E11.9  Without complications
```

## 各國臨床修訂版

| 版本 | 用途 | 使用地 |
| --- | --- | --- |
| ICD-10-CM | 診斷（比 WHO 版更細，最長 7 碼） | 美國；台灣健保自 2016 年起 |
| ICD-10-PCS | 住院處置（7 碼英數，與診斷碼結構不同） | 美國；台灣健保住院處置 |
| ICD-9-CM | 舊版診斷 / 處置 | 美國 2015-10 前、台灣 2016 前的資料 |

## 用 ICD 做研究的注意事項

| 注意 | 說明 |
| --- | --- |
| 申報偏差 | 代碼反映給付規則與編碼習慣，不一定等於臨床真實診斷；用多個條件（≥2 次門診、搭配用藥 / 檢驗）提高特異度 |
| 版本切換 | 跨越 ICD-9 → ICD-10 的世代要合併兩套代碼清單，切換點附近盛行率常出現跳動 |
| 主 / 次診斷 | 住院資料區分主診斷與次診斷，定義疾病時要決定用哪一種 |
| 罕病 | 許多罕病沒有專屬 ICD 代碼，可補用 [Orphanet](../../genetics/databases/gene-disease-association/orphanet.md) 的 ORPHA code |
| 對應 | ICD → SNOMED CT 常一對多；分析平台如 [OMOP-CDM](omop-cdm.md) 會把 ICD 當來源碼，再對到 SNOMED 標準概念 |
