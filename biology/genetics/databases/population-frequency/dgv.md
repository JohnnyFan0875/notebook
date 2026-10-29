[資料庫](../README.md) › [族群頻率](README.md) › DGV

# DGV (Database of Genomic Variants)

收錄**健康人**結構變異（CNV、大型插入 / 缺失、倒位）的資料庫，判讀 CNV 時用來檢查某個缺失 / 重複是否常見於一般族群。

| 項目 | 內容 |
| --- | --- |
| 網站 | [dgv.tcag.ca](https://dgv.tcag.ca/)（[下載頁](https://dgv.tcag.ca/dgv/app/downloads)） |
| 維護 | The Centre for Applied Genomics（多倫多 SickKids） |
| 資料 | 從已發表研究彙整的健康對照 SV；另有整合多研究的 **DGV Gold Standard** 變異集 |
| 版本 | GRCh37、GRCh38 |

| 使用注意 | 說明 |
| --- | --- |
| 早期研究的解析度低 | 許多記錄來自晶片 (array CGH / SNP array)，邊界不精確、大小被高估 |
| 不是頻率資料庫 | 單一研究、樣本數不一；優先看 Gold Standard 或多研究重複出現的變異 |
| 重疊 ≠ 相同 | 檢查重疊比例、方向（缺失 vs 重複）與是否涵蓋關鍵基因 |

## CNV 判讀的其他資源

| 資源 | 用途 |
| --- | --- |
| gnomAD-SV | 定序資料的 SV 族群頻率（見 [gnomAD](gnomad.md)） |
| ClinGen Dosage Sensitivity | 基因 / 區域的單倍劑量不足與三倍劑量敏感度評分 |
| DECIPHER | 病人的 CNV 與表型（罕病） |
| ClinVar | 已提交的 CNV 臨床分類 |
| ACMG / ClinGen CNV 準則 | 計分式的 CNV 分類（Riggs et al. 2020） |
