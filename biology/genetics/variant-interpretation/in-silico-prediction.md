[遺傳學](../README.md) › [變異判讀](README.md) › In-silico 預測

# In-silico 預測工具 (In-silico Prediction Tools)

用計算方法預測變異對蛋白質功能或剪接的影響，在 ACMG/AMP 中對應 **PP3**（預測有害）與 **BP4**（預測無影響）。預測只是支持性證據，不能單獨決定分類。

## 錯義變異 (missense)

| 工具 | 範圍 | 方向 / 常用閾值 | 特點 |
| --- | --- | --- | --- |
| REVEL | 0–1 | 高 = 有害；校準閾值見下表 | 整合多個工具的 meta-predictor；ClinGen 校準最完整 |
| AlphaMissense | 0–1 | > 0.564 可能致病、< 0.34 可能良性（原作者分類） | DeepMind；以蛋白結構與演化訓練 |
| BayesDel（不含頻率） | 約 −1.29–0.76 | 高 = 有害 | ClinGen 校準工具之一 |
| CADD | PHRED 0–99 | ≥ 20 約為基因組最有害的前 1% | 也可評估非編碼變異 |
| SIFT | 0–1 | **< 0.05 有害**（方向相反） | 演化保守性 |
| PolyPhen-2 | 0–1 | 高 = 有害 | 結構與保守性 |
| PrimateAI | 0–1 | > 0.803 有害 | 以靈長類常見變異訓練 |
| MutationAssessor | 約 −5.1–6.5 | > 3.5 高度有害 | |
| FATHMM | 約 −16–11 | **< −1.5 有害**（方向相反） | |
| 保守性：GERP++、phyloP | — | GERP > 4.4 高度保守 | 不是致病預測，只看保守 |

## 剪接

| 工具 | 範圍 | 用法 |
| --- | --- | --- |
| SpliceAI | 0–1（Δ score） | 最常用；ClinGen 建議 ≥ 0.2 支持 PP3、≤ 0.1 支持 BP4 |
| MaxEntScan | 剪接位點強度 | 比較 REF / ALT 的分數變化 |
| dbscSNV（Ada / RF） | 0–1 | 剪接區 SNV 的機率 |
| [varSEAK](https://varseak.bio/) JSI | 剪接位點品質分數 | 評估 5′ / 3′ 剪接位點（含分支點、多嘧啶區）；網站報告在非 GT/AG 位置的變異上優於 MaxEntScan，偽陽性的新剪接位點需比較 REF / ALT 分數過濾 |

## ClinGen 校準：一個工具、依分數給強度

Pejaver et al.（2022）用已知致病 / 良性變異校準，建議**只選一個**經校準的工具，依分數給 PP3 / BP4 不同強度（不再要求「多個工具一致」）。

| REVEL 分數 | 證據 |
| --- | --- |
| ≥ 0.932 | PP3_Strong |
| ≥ 0.773 | PP3_Moderate |
| ≥ 0.644 | PP3_Supporting |
| 0.291–0.643 | 無證據（不確定） |
| ≤ 0.290 | BP4_Supporting |
| ≤ 0.183 | BP4_Moderate |
| ≤ 0.016 | BP4_Strong |

> 不要把多個高度相關的工具重複計分（REVEL 本身已整合 SIFT、PolyPhen 等）；PP3 與 PM1、PS1 等同樣基於「位置 / 胺基酸」的證據合併使用時，ClinGen 建議設上限避免重複計算。

## 使用注意

| 注意 | 說明 |
| --- | --- |
| 方向不同 | SIFT、FATHMM 是越低越有害；其他多半越高越有害 |
| 訓練資料循環 | 部分工具用 ClinVar 訓練，拿來判讀 ClinVar 中的變異有循環論證的問題 |
| 基因專一表現 | 一般閾值在某些基因（如離子通道、心臟基因）表現不佳；有專用工具（如 CardioBoost）與 VCEP 規格時優先使用 |
| 版本 | 工具與分數會更新，報告記錄版本 |

取得方式：VEP 外掛或 dbNSFP 一次取得多數分數，見 [Ensembl VEP](../databases/variant/ensembl-vep.md)。分數範圍整理參考：[Genoox：Prediction tools and score range](https://help.genoox.com/en/articles/4341424-prediction-tools-and-score-range)。
