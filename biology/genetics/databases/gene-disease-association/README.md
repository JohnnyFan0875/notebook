[遺傳學](../../README.md) › [資料庫](../README.md) › 基因–疾病關聯

# 基因–疾病關聯資料庫 (Gene–Disease Association Databases)

判讀一個變異前，要先確認「這個基因真的會造成這個疾病嗎？證據多強？遺傳模式是什麼？」。基因–疾病關聯薄弱時，即使變異看起來很有害，也只能報 VUS。

## 依用途

| 資料庫 | 用途 | 何時用 |
| --- | --- | --- |
| [OMIM](omim.md) | 基因與孟德爾疾病的權威目錄、遺傳模式 | 這個基因與哪些疾病有關？什麼遺傳模式？ |
| [ClinGen](clingen-validity.md) | 基因–疾病有效性分級、劑量敏感度、專家小組規格 | 關聯證據多強？CNV 劑量是否致病？ |
| [GenCC](gencc.md) | 多個機構的基因–疾病分級彙整 | 一次看各機構的評級是否一致 |
| [PanelApp](genomics-england-panelapp.md) | 專家審閱的疾病 panel（綠 / 黃 / 紅） | 某疾病該檢測哪些基因？ |
| [GeneReviews](gene-reviews.md) | 疾病的臨床總覽：診斷、處置、遺傳諮詢 | 臨床面的完整背景 |
| [HPO](hpo.md) | 標準化的表型詞彙與基因–表型註解 | 依病人表型排序候選基因 |
| [Orphanet](orphanet.md) | 罕見疾病分類、盛行率、專家與藥物 | 罕病的命名、分類、編碼對照 |
| [HGMD](hgmd.md) | 文獻報告的致病變異 | 補充文獻中的變異 |
| [DisGeNET](disgenet.md) | 整合審閱資料與文獻探勘的基因–疾病關聯 | 複雜疾病、研究探索 |
| [CGD](clinical-genomic-database.md) | 有臨床介入措施的基因 | 結果是否「可處置」(actionable)？ |
| [MARRVEL](marrvel.md) | 人類資料 + 模式生物資源整合 | 罕病候選基因 / 變異的功能證據 |
| [罕見疾病一點通](rare-disease-taiwan.md) | 台灣罕見疾病的中文衛教資訊 | 台灣罕病的病人資源與公告名單 |

## 判讀流程中的位置

```
病人表型（HPO 詞彙）
  → 候選基因（PanelApp / OMIM / 表型排序工具如 Exomiser）
  → 基因–疾病有效性（ClinGen / GenCC：Definitive / Strong / Moderate / Limited…）
  → 遺傳模式是否相符（OMIM、GeneReviews）
  → 變異層級判讀（ClinVar、族群頻率、ACMG/AMP）
```

> 證據等級為 Limited、Disputed、Refuted 的基因，不應用來報告致病結果。panel 設計也應以有效性分級為準，見 [標靶定序](../../../genomics/sequencing-techniques/targeted-panels.md)。
