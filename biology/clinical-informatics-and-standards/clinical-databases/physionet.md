[臨床資訊與標準](../README.md) › [臨床資料庫](README.md) › PhysioNet

# PhysioNet

MIT LCP 維護的生醫資料平台，提供生理訊號（ECG、EEG、ICU 波形）、臨床資料庫與 PhysioNet Challenge 競賽資料。MIMIC 與 eICU 都從這裡申請下載。

| 項目 | 內容 |
| --- | --- |
| 網站 | [physionet.org](https://physionet.org) |
| 資料類型 | 開放資料（多數波形資料庫）、需登入、credentialed（MIMIC、eICU 等含病歷資料） |
| 雲端存取 | 部分資料集可經 Google BigQuery / GCS、AWS 存取 |
| Python 工具 | `wfdb`（讀寫 WFDB 格式的波形與註解） |

## 取得 credentialed 資料

```
1. 註冊 PhysioNet 帳號
2. 申請 credentialing（填寫研究用途、提供推薦人 / 指導者）
3. 完成 CITI「Data or Specimens Only Research」線上訓練，上傳證書
4. 在每個資料集頁面簽署 Data Use Agreement（PhysioNet Credentialed Health Data License）
5. 下載，或連結 BigQuery
```

## 使用規範

| 規範 | 說明 |
| --- | --- |
| 不可分享 | 帳號與資料都不能給未簽 DUA 的人，包括實驗室同事 |
| LLM / 線上服務 | 不能把 credentialed 資料送進會保存資料、用於訓練或有人工審閱的第三方服務；建議用本地部署的模型，雲端 API 須確認零資料保留 |
| 不可再識別 | 不可嘗試辨識病人身分 |
| 發表 | 引用資料集 DOI 與原始論文；分享程式碼（不含資料） |

```python
import wfdb

# 直接從 PhysioNet 讀取 MIT-BIH 心律不整資料庫的第 100 筆（開放資料）
record = wfdb.rdrecord("100", pn_dir="mitdb")
ann = wfdb.rdann("100", "atr", pn_dir="mitdb")
record.p_signal.shape   # (650000, 2)：360 Hz × 30 分鐘，2 導程
record.fs               # 360
```

LLM 使用醫療資料的其他注意事項見 [生醫 LLM](../../../data-science/llm/bio-and-medical-llm.md)。
