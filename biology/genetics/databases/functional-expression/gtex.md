[資料庫](../README.md) › [功能與表現](README.md) › GTEx

# GTEx (Genotype-Tissue Expression)

從約 1,000 位已故捐贈者採集約 50 種非疾病組織，做全基因組定序與 RNA-seq，提供人體組織的基因表現圖譜與 eQTL / sQTL，是解讀非編碼變異最常用的參考。

| 項目 | 內容 |
| --- | --- |
| 入口 | [GTEx Portal](https://gtexportal.org/) |
| 資料 | 各組織的 TPM 表現量、cis-eQTL / sQTL、fine-mapping 結果、單細胞（部分組織） |
| 存取 | 表現量與 QTL 摘要公開下載；個人層級的基因型與原始 reads 需 dbGaP 申請 |
| 版本 | 以 v8 / v10 最常被引用；引用時註明版本 |

| 用途 | 怎麼看 |
| --- | --- |
| 基因是否在疾病相關組織表現 | Gene 頁面的組織表現量 violin plot |
| 變異是否為 eQTL / sQTL | Variant 頁面：各組織的效應量 (NES) 與 p 值 |
| GWAS 位點的目標基因 | 與 eQTL 做 [colocalization](../../../genomics/genome-wide-analysis/colocalization.md) |

| 限制 | 說明 |
| --- | --- |
| 死後組織 | 缺血時間與死因影響表現量 |
| bulk 組織 | 細胞組成差異會混入表現量與 eQTL |
| 樣本以歐裔為主 | eQTL 在其他族群的可轉移性有限 |
| 非疾病組織 | 疾病狀態下的調控可能不同 |

相關：[eQTL](../../../genomics/genome-wide-analysis/eqtl.md)、[sQTL](../../../genomics/genome-wide-analysis/sqtl.md)。
