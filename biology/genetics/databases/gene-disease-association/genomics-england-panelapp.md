[資料庫](../README.md) › [基因–疾病關聯](README.md) › PanelApp

# Genomics England PanelApp

英國 Genomics England 的群眾審閱平台：各疾病 panel 列出相關基因，由專家依證據標示等級。用於英國 NHS 基因檢測與 10 萬人基因組計畫的判讀。

| 項目 | 內容 |
| --- | --- |
| 網站 | [panelapp.genomicsengland.co.uk](https://panelapp.genomicsengland.co.uk/)；另有 [PanelApp Australia](https://panelapp.agha.umccr.org/) |
| 存取 | 網頁、REST API、TSV 下載；panel 有版本號 |
| 內容 | 每個基因的等級、遺傳模式、致病機制、證據來源與審閱意見；也包含 STR 與 CNV 區域 |

| 等級 | 意義 |
| --- | --- |
| 綠 (Green) | 診斷等級：證據充分，可用於臨床報告 |
| 黃 (Amber) | 證據中等，研究或特殊情況才納入 |
| 紅 (Red) | 證據不足 |

> 設計或篩選 panel 時常用「只取綠色基因」；引用時記錄 panel 名稱與版本。相關：[標靶定序](../../../genomics/sequencing-techniques/targeted-panels.md)。
