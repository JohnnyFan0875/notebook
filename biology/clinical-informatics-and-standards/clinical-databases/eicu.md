[臨床資訊與標準](../README.md) › [臨床資料庫](README.md) › eICU

# eICU Collaborative Research Database

eICU-CRD 來自 Philips eICU 遠距加護照護計畫，收錄美國多家醫院的 ICU 住院資料。和單一中心的 [MIMIC-IV](mimic-iv.md) 互補，常用來做多中心比較與外部驗證。

| 項目 | 內容 |
| --- | --- |
| 網站 | [physionet.org/content/eicu-crd](https://physionet.org/content/eicu-crd/)、文件 [eicu-crd.mit.edu](https://eicu-crd.mit.edu) |
| 版本 | v2.0（2019） |
| 範圍 | 2014–2015 年，美國 208 家醫院、335 個 ICU，超過 20 萬次 ICU 住院、約 13.9 萬病人 |
| 申請 | 同 MIMIC：PhysioNet credentialing + CITI 訓練 + DUA，見 [PhysioNet](physionet.md) |
| 程式碼 | [eicu-code](https://github.com/MIT-LCP/eicu-code) |

## 主要資料表

| 資料表 | 內容 |
| --- | --- |
| `patient` | 每次 ICU 住院一列（`patientunitstayid`）、醫院、入出 ICU 資訊 |
| `hospital` | 醫院規模、地區、是否教學醫院 |
| `apachepatientresult`、`apacheapsvar` | APACHE IV 分數與預測死亡率 |
| `vitalperiodic`、`vitalaperiodic` | 定期 / 不定期生命徵象 |
| `lab` | 檢驗值 |
| `medication`、`infusiondrug` | 用藥、點滴 |
| `diagnosis`、`treatment`、`pasthistory` | 診斷、處置、病史 |

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 時間是 offset | 時間欄位是相對入 ICU 的**分鐘數**（`*offset`，可為負值），沒有日期 |
| 各院完整度不一 | 有些醫院某些資料表幾乎沒有資料；先依醫院檢查缺值，必要時排除或在模型中加入醫院效應 |
| 單位與名稱 | `lab` 用文字名稱（`labname`），需自行標準化 |
| 年齡 | 大於 89 歲記為 `> 89` 字串 |
