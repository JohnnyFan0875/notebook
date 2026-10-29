[Biology](../../README.md) › [臨床資訊與標準](../README.md) › 臨床資料庫

# 臨床資料庫 (Clinical Databases)

可申請使用的去識別化病歷與世代資料，常用於建立世代 (cohort building)、預測模型與基因–表型關聯研究。這些資料都需要申請與簽署資料使用協議 (DUA)，不能任意分享或上傳到外部服務。

| 資源 | 內容 | 何時用 |
| --- | --- | --- |
| [PhysioNet](physionet.md) | 生理訊號與臨床資料庫的平台，MIMIC、eICU 的入口 | 申請 credentialed 資料、取得波形 / ECG 資料 |
| [MIMIC-IV](mimic-iv.md) | 單一醫學中心（BIDMC）的急診、住院、ICU 病歷 | 重症與住院研究、臨床 ML 練習與 benchmark |
| [eICU](eicu.md) | 美國 208 家醫院的 ICU 資料（2014–2015） | 多中心比較、外部驗證 |
| [UK Biobank](uk-biobank.md) | 50 萬名英國成人的基因型、影像、問卷與病歷連結 | GWAS、PRS、基因–環境、蛋白質體 |

## 比較

| 項目 | MIMIC-IV | eICU | UK Biobank |
| --- | --- | --- | --- |
| 族群 | 住院與 ICU 病人 | ICU 病人 | 40–69 歲招募的社區成人 |
| 規模 | 約 36 萬病人 | 約 20 萬次 ICU 住院 | 約 50 萬人 |
| 基因資料 | 無 | 無 | 基因型晶片、全外顯子、全基因組 |
| 申請 | PhysioNet credentialing + CITI 訓練 | 同左 | 研究計畫申請 + 付費 |
| 費用 | 免費 | 免費 | 需付存取費與雲端運算費 |
| 主要偏差 | 單一中心、教學醫院 | 各院紀錄完整度不一 | 較健康、較高社經（healthy volunteer bias） |

> 病歷資料的時間欄位、編碼版本、缺值機制都和研究結論有關。選擇偏誤見 [資料偏誤與代表性](../../../data-science/responsible-ai/data-bias-and-representativeness.md)，去識別化規範見 [隱私與法規](../../../data-science/responsible-ai/privacy-and-regulation.md#hipaa-去識別化)。
