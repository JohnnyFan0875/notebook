[基因體學](../../README.md) › [分析流程](../README.md) › RNA-seq

# RNA-seq 分析 (Bulk RNA-seq Analysis)

從原始 FASTQ 到差異表現與功能富集的 bulk RNA-seq 教學：每一步做什麼、為什麼、怎麼檢查結果。工具選擇與參數參考一套實際使用的 RNA-seq pipeline，但教學本身以 Bash / R / Python 分段呈現，不依賴工作流引擎。單細胞見 [單細胞 RNA-seq](../../sequencing-techniques/single-cell-rna-seq/README.md)。

## 建議順序

| 章 | 內容 | 回答的問題 |
| --- | --- | --- |
| [01 概觀](01-rnaseq-overview.md) | bulk vs 單細胞、表現量層級、library 類型、重複、count matrix | RNA-seq 能回答什麼？ |
| [02 FASTQ QC](02-fastq-quality-control-and-trimming.md) | 完整性檢查、FastQC / MultiQC、fastp 修剪 | 原始資料能用嗎？要不要修剪？ |
| [03 比對](03-reference-alignment-and-bam-qc.md) | 參考版本、STAR / HISAT2、BAM 處理、比對 QC | reads 對到哪裡？比對品質如何？ |
| [04 定量](04-pseudoalignment-counting-and-tximport.md) | Salmon / kallisto、featureCounts、tximport | 怎麼得到每個基因的 counts？ |
| [05 標準化](05-count-matrix-filtering-normalization.md) | metadata 對齊、低表現過濾、CPM / TPM / TMM / median-of-ratios | 樣本間怎麼比較？ |
| [06 EDA 與設計](06-exploratory-design-and-count-models.md) | PCA / 相關熱圖、設計矩陣、負二項模型 | 樣本結構合理嗎？模型怎麼設？ |
| [07 差異表現](07-differential-expression.md) | edgeR、DESeq2、limma-voom 與比較 | 哪些基因表現改變？ |
| [08 對比與視覺化](08-contrasts-testing-and-visualization.md) | 對比方向、交互作用、FDR、MA / volcano / heatmap | 結果怎麼解讀與呈現？ |
| [09 富集分析](09-annotation-and-functional-enrichment.md) | ID 轉換、ORA、GSEA（clusterProfiler） | 這些基因代表哪些生物過程？ |
| [10 可重現性](10-reproducibility-and-troubleshooting.md) | 環境、版本、常見錯誤排除 | 結果能被重現嗎？出錯怎麼查？ |

## 資料夾內容

```text
rna-seq/
├── README.md、01–10 章
├── data/      # 模擬的 count matrix、metadata、DE 與富集結果
├── scripts/   # Bash（QC、修剪、比對、定量）、R（edgeR、DESeq2、limma-voom、tximport、富集）、Python（模擬資料與圖）
└── src/       # 各章的圖
```

`data/` 與 `src/` 的資料和圖由 `scripts/simulate_rnaseq_demo.py` 產生，只用來示範流程，**不代表真實生物學發現**。

```bash
# 在 notebook 根目錄執行；需要 numpy、pandas、matplotlib
python biology/genomics/workflows/rna-seq/scripts/simulate_rnaseq_demo.py \
  --outdir biology/genomics/workflows/rna-seq
```

## 驗證狀態

| 項目 | 狀態 |
| --- | --- |
| `simulate_rnaseq_demo.py` | 實跑；固定 seed 可重現相同資料 |
| `metadata_design_checks.R`、`edger_workflow.R`、`deseq2_workflow.R`、`limma_voom_workflow.R` | 以 R 4.6.1 / Bioconductor 3.23 在模擬資料上實跑 |
| 09 章的 clusterProfiler 程式碼 | 以 airway 真實資料實跑（模擬資料的基因名無法對應真實基因） |
| `tximport_to_gene.R`、所有 Bash 腳本 | 未實跑：需要 Salmon 輸出、FASTQ、參考基因組與 STAR / HISAT2 / fastp 等工具；參數已對照官方文件 |

相關統計：[GLM 計數模型](../../../../data-science/statistics/regression-analysis/glm-count-models.md)、[多重檢定](../../../../data-science/statistics/inferential-statistics/multiple-testing.md)、[PCA](../../../../data-science/statistics/multivariate-analysis/pca.md)、[批次效應](../../../../data-science/statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)。
