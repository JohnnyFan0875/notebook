# RNA-seq Analysis

這套筆記是一份從原始 FASTQ 到 differential expression 與 functional enrichment 的 RNA-seq 教學。內容參考 `/home/johnny_fan/project/rna_seq_pipeline` 的工具選擇、參數習慣、測試資料命名與輸出型態，但教學本身不以 Nextflow 為主軸，也不要求讀者透過 workflow manager 執行。

本教學的核心問題是：如何讓具有基礎生物資訊背景的讀者，從 reads、reference、quantification、count matrix、normalization、statistical model 到 biological interpretation，逐步知道每一步在做什麼、為什麼做、如何檢查結果。

**使用資料：**

- FASTQ、FastQC、fastp 與 Salmon 輸出格式說明參考 RNA-seq pipeline 的小型測試專案。
- `data/` 與 `src/` 中的 count matrix、metadata、DE result、enrichment result 與 PNG 圖檔由 `scripts/simulate_rnaseq_demo.py` 產生。
- 本教學的模擬資料僅用於展示分析流程，結果不代表真實生物學研究發現。

## Suggested Reading Order

1. [RNA-seq Overview](./01-rnaseq-overview.md)
2. [FASTQ, Quality Control, and Trimming](./02-fastq-quality-control-and-trimming.md)
3. [Reference Genome, Alignment, BAM, and Alignment QC](./03-reference-alignment-and-bam-qc.md)
4. [Pseudoalignment, Read Counting, and tximport](./04-pseudoalignment-counting-and-tximport.md)
5. [Count Matrix, Filtering, Normalization, and TMM](./05-count-matrix-filtering-normalization.md)
6. [Exploratory Analysis, Experimental Design, and Count Models](./06-exploratory-design-and-count-models.md)
7. [Differential Expression: edgeR, DESeq2, and limma-voom](./07-differential-expression.md)
8. [Contrasts, Multiple Testing, and DE Visualization](./08-contrasts-testing-and-visualization.md)
9. [Gene Annotation and Functional Enrichment](./09-annotation-and-functional-enrichment.md)
10. [Reproducibility and Troubleshooting](./10-reproducibility-and-troubleshooting.md)

## Directory Layout

```text
rna-seq/
├── index.md
├── 01-rnaseq-overview.md
├── 02-fastq-quality-control-and-trimming.md
├── 03-reference-alignment-and-bam-qc.md
├── 04-pseudoalignment-counting-and-tximport.md
├── 05-count-matrix-filtering-normalization.md
├── 06-exploratory-design-and-count-models.md
├── 07-differential-expression.md
├── 08-contrasts-testing-and-visualization.md
├── 09-annotation-and-functional-enrichment.md
├── 10-reproducibility-and-troubleshooting.md
├── data/
├── scripts/
└── src/
```

## Reproduce the Demo Data and Figures

```bash
cd /home/johnny_fan/project/notebook
MPLCONFIGDIR=/tmp/matplotlib-rnaseq \
python biology/genomics/sequencing-and-analysis/workflows/rna-seq/scripts/simulate_rnaseq_demo.py
```

主要輸出：

- `data/simulated_gene_counts.csv`
- `data/sample_metadata.csv`
- `data/simulated_de_results.csv`
- `data/simulated_enrichment_results.csv`
- `src/*.png`

## What Is Executable Here

Python demo script 已在目前環境實際執行並產生圖檔。Bash 與 R scripts 是完整教學腳本，但依賴外部工具或 Bioconductor 套件；目前環境缺少 `Rscript`，因此 R scripts 尚未在本機驗證執行。

