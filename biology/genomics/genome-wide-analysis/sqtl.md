[基因體學](../README.md) › [全基因體分析](README.md) › sQTL

# 剪接 QTL (Splicing QTL, sQTL)

與 RNA 剪接型態相關的遺傳變異：改變 exon 使用、剪接位點選擇或 isoform 比例。有些疾病機制在「總表現量」上看不出來，只在剪接層級出現，所以 sQTL 常與 eQTL 一起分析。

| 表型的量法 | 工具 | 說明 |
| --- | --- | --- |
| intron excision 比例 | LeafCutter | 由跨剪接 reads 定義 intron cluster，不依賴註解，可找新的剪接事件；GTEx 採用 |
| PSI（percent spliced in） | rMATS、SUPPA2 | 依已知事件類型（exon skipping、alternative 5′ / 3′ 等） |
| isoform 比例 | Salmon + DTU 方法 | 依轉錄本註解 |

| 要點 | 說明 |
| --- | --- |
| 需要跨剪接的 reads | read 長度與深度影響可量化的事件數 |
| 剪接位點附近的變異 | 直接破壞 GT-AG 共通序列，效應通常最大；深層 intron 變異也可能創造新的剪接位點 |
| 與預測工具互補 | SpliceAI 等預測單一變異對剪接的影響，見 [in-silico 預測](../../genetics/variant-interpretation/in-silico-prediction.md) |

統計框架（共變數、permutation + FDR）同 eQTL，見 [QTL 分析：相關統計方法](qtl-analysis-and-mapping.md#相關統計方法)；比對與剪接 reads 見 [RNA-seq 03](../workflows/rna-seq/03-reference-alignment-and-bam-qc.md)。
