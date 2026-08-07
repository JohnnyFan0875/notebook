# RNA-seq Overview

**RNA-seq** 用 high-throughput sequencing 讀出樣本中的 RNA 分子，再用 read mapping、quantification 與統計模型推估基因或轉錄本的表達變化。它可以回答的問題包括：

- 不同處理、疾病、組織或時間點之間，哪些基因表達量改變？
- 樣本是否依 biological condition 聚集，或主要被 batch effect 驅動？
- 某些 pathway、gene set 或 biological process 是否整體上調或下調？
- transcript isoform usage、alternative splicing 或 novel transcript 是否改變？
- 表達量變化是否可與 phenotype、genotype、drug response 或臨床變項連結？

Key point: RNA-seq analysis 不是單一軟體步驟，而是一連串資料品質、參考版本、定量單位、模型假設與 biological interpretation 的選擇。

## Bulk RNA-seq and Single-cell RNA-seq

| Topic | Bulk RNA-seq | Single-cell RNA-seq |
| --- | --- | --- |
| 樣本單位 | 一個樣本通常是細胞群平均訊號 | 每個 cell 或 nucleus 是觀測單位 |
| 主要問題 | group-level differential expression | cell type、trajectory、cell-state heterogeneity |
| Count 特性 | replicate 間 biological variation 是核心 | dropout、UMI、cell QC 與 batch integration 更關鍵 |
| 常用方法 | STAR/HISAT2/Salmon/kallisto + edgeR/DESeq2/limma | Cell Ranger/STARsolo/alevin-fry + Seurat/Scanpy |
| 解讀 | 基因表達平均差異 | cell composition 與 cell-state 混合效應 |

本教學聚焦 **bulk RNA-seq**。Single-cell RNA-seq 的概念與檔案格式有重疊，但 QC、normalization、統計單位與 differential expression 的陷阱不同，不應直接套用 bulk workflow。

## Expression Levels

| Level | Meaning | Common output |
| --- | --- | --- |
| Gene expression | 同一 gene 底下 exon 或 transcript 訊號彙整 | gene count matrix、gene TPM |
| Transcript expression | 每個 transcript model 的 abundance | Salmon/kallisto `quant.sf` 或 `abundance.tsv` |
| Isoform expression | transcript usage 或 isoform proportion | transcript TPM、DTU/DEXSeq/DRIMSeq results |

Gene-level differential expression 不等於 isoform switching。若研究問題是 alternative splicing、transcript usage 或 isoform-specific regulation，應保留 transcript-level 或 junction-level information。

## Reads, Fragments, and Library Types

**Read** 是 sequencer 實際讀出的 sequence。**Fragment** 是 library 中原始 cDNA 片段；paired-end sequencing 會從同一 fragment 兩端產生 R1 與 R2。對 paired-end RNA-seq 做 gene-level counting 時，通常應 count fragments 而不是把兩端 read 各算一次。

| Concept | Practical implication |
| --- | --- |
| Single-end | 一個 fragment 只有一端 read，便宜但對 mapping 與 isoform 解析較弱 |
| Paired-end | 可估 insert size、提高 splice junction 與 transcript ambiguity 判斷 |
| Strand-specific | read 方向保留 transcript strand 資訊，featureCounts `-s`、Salmon library type 必須設對 |
| Unstranded | read 方向不保留來源 strand，antisense 或 overlapping gene 較難處理 |

Warning: strandness 設錯常造成 featureCounts assignment 極低，或 sense/antisense gene 訊號被錯誤歸類。

## Replicates, Depth, and Library Size

**Biological replicate** 是獨立生物樣本，例如不同個體或獨立培養批次。**Technical replicate** 是同一 RNA/library 的技術重複，例如同一樣本重上機。RNA-seq differential expression 的變異主要來自 biological replicate，因此不能把 technical replicate 當成 biological replicate。

**Sequencing depth** 是樣本取得多少 reads/fragments。**Library size** 在 count matrix 中通常指每個樣本所有 feature counts 的總和。兩者相關但不完全相同，因為 reads 可能 unmapped、落在 rRNA、intronic/intergenic region，或被過濾。

## Count Matrix

Count matrix 通常是 gene-by-sample：

```text
gene_id        ctrl_1  ctrl_2  ctrl_3  treat_1  treat_2  treat_3
ENSG000001       102      88     111      190      205      177
ENSG000002         0       1       0        0        2        0
ENSG000003      5200    6120    5801     5900     6012     6220
```

欄位是 sample，列是 gene 或 transcript。主分析用的 count 應是非負整數或可合理四捨五入的 estimated counts；TPM/FPKM/RPKM 不應直接當作 edgeR 或 DESeq2 的 count input。

## Full Workflow

```text
FASTQ
  -> FastQC / MultiQC
  -> trimming if needed
  -> reference genome and annotation check
  -> STAR/HISAT2 alignment or Salmon/kallisto lightweight mapping
  -> BAM QC or transcript quantification QC
  -> featureCounts/HTSeq-count or tximport
  -> count matrix + sample metadata checks
  -> filtering and normalization
  -> exploratory analysis
  -> experimental design and count model
  -> differential expression
  -> annotation and enrichment
  -> reproducible report
```

Tip: 不同方法不是線性取代關係。STAR/HISAT2 產生 BAM，適合 alignment QC、variant calling、fusion 或 novel transcript discovery；Salmon/kallisto 快速產生 transcript abundance，適合 transcript-level quantification 與 gene-level DE import。

