[遺傳學](../README.md) › [基礎概念](README.md) › 新生變異

# 新生變異 vs 未見變異 (De Novo vs Novel Variant)

兩個名詞常被混用，但意義不同：

| | 新生變異 (de novo) | 未見變異 (novel) |
| --- | --- | --- |
| 定義 | 先證者 (proband) 帶有、**親生父母都沒有**的變異 | 在比較用的資料庫中**沒有出現過**的變異 |
| 如何確認 | 親子三人組 (trio) 定序，並確認親子關係 | 查 gnomAD、dbSNP、ClinVar |
| 判讀意義 | 嚴重、早發的顯性疾病中是很強的致病證據（ACMG PS2 / PM6） | 只代表罕見（PM2，現多為 Supporting），不代表致病 |

一個變異可以是 novel 但不是 de novo（父母之一也帶有），也可以是 de novo 但不是 novel（同一個突變在其他人身上也獨立發生過，如熱點突變）。

## 背景數字

| 項目 | 數值 |
| --- | --- |
| 每代每個鹼基的突變率 | 約 1.2 × 10⁻⁸ |
| 每個人的新生 SNV | 約 60–70 個（全基因組），其中編碼區約 1–2 個 |
| 父親年齡效應 | 父親每大 1 歲，約多 1–2 個新生變異（精原細胞持續分裂） |
| 疾病角色 | 嚴重發展遲緩、智能障礙、自閉症、癲癇性腦病中，新生變異是主要病因之一 |

## 判讀要點

| 要點 | 說明 |
| --- | --- |
| 確認親子關係 | 未確認時只能用 PM6（假定新生），強度較低 |
| 排除父母的低比例嵌合 | 父母 VAF 很低的嵌合可能被當成「沒有」；檢查父母該位置的深度與 reads（[IGV](../../bioinformatics-tools/visualization/igv.md)） |
| 先證者本身的嵌合 | VAF 明顯低於 50% 時考慮受精後突變 |
| 偽陽性 | 父母該位置深度不足、比對假象都會造成假的新生變異；用專門工具（DeNovoGear、GATK PossibleDeNovo、Slivar）並人工複核 |
| 表型相符 | ClinGen 依表型專一性與確認程度給 PS2 / PM6 不同點數 |
| 再發風險 | 一般低（約 1–2%），但父母生殖腺嵌合時會較高 |

相關：[ACMG/AMP](../variant-interpretation/acmg-amp.md)、[變異等位基因頻率](variant-allele-frequency.md)、[族群頻率資料庫](../databases/population-frequency/README.md)。
