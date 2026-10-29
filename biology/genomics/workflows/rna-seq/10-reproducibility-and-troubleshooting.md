# Reproducibility and Troubleshooting

本章目的：整理 RNA-seq project 的環境、路徑、版本、log 與常見錯誤。這些內容不是形式問題，而是 RNA-seq 結果能否重現與被正確解讀的基礎。

## Reproducibility

建議專案目錄：

```text
project/
├── data/
│   ├── raw/
│   ├── reference/
│   └── metadata/
├── results/
│   ├── fastqc/
│   ├── trimming/
│   ├── alignment/
│   ├── counts/
│   ├── de/
│   └── enrichment/
├── scripts/
├── logs/
└── README.md
```

應保存：

| Item | Why |
| --- | --- |
| Software versions | STAR/HISAT2/Salmon/featureCounts/edgeR/DESeq2 版本會影響結果 |
| Conda environment | 讓 command-line tools 可重建 |
| R `sessionInfo()` | 保存 Bioconductor 與 annotation package 版本 |
| `renv.lock` | R package environment lock |
| Container | 對長期重現最穩 |
| Random seed | PCA label jitter、bootstrap、simulation、GSEA permutation 需固定 |
| Relative paths | 避免專案搬移後失效 |
| Logs | FastQC、fastp、STAR、HISAT2、featureCounts、DE scripts |
| Git | script versioning 與 review |
| Metadata | sample sheet、batch、RIN、library prep、sequencing run |
| Reference genome version | FASTA、GTF、transcriptome、tx2gene 來源與 release |

Conda 範例：

```bash
conda create -n rnaseq -c conda-forge -c bioconda \
  fastqc multiqc fastp star hisat2 salmon kallisto samtools subread r-base
conda activate rnaseq
```

R session：

```r
writeLines(capture.output(sessionInfo()), "results/sessionInfo.txt")
```

`renv`：

```r
install.packages("renv")
renv::init()
renv::snapshot()
```

Workflow manager 的價值是把步驟依賴、版本、重跑條件與平行化管理起來；但本教學故意以 Bash/R/Python 分段呈現，讓讀者先理解每個分析步驟本身。

## Troubleshooting Table

| Problem | Symptom | Likely cause | Check / Fix |
| --- | --- | --- | --- |
| FASTQ incomplete | gzip EOF、行數非 4 倍數 | 下載中斷或傳輸錯誤 | `md5sum`、重新下載 |
| Paired-end reads 不成對 | aligner 報 read pair mismatch | R1/R2 混樣或排序錯 | 比對 read id，重新取得 pairs |
| Adapter 未移除 | FastQC adapter content 高 | insert 短、read-through | fastp/Cutadapt trimming |
| Reference/GTF 不一致 | mapping 或 counting 異常 | assembly release 混用 | 檢查 release、chrom names |
| `chr1` vs `1` | featureCounts assign 很低 | chromosome naming style 不同 | 統一 FASTA/GTF/BAM naming |
| Mapping rate 低 | STAR/HISAT2 uniquely mapped 低 | 污染、錯物種、低品質、短 reads | FastQC、Kraken/FastQ Screen、reference check |
| rRNA reads 高 | exonic protein-coding reads 低 | rRNA depletion 失敗 | RSeQC/Picard RNA metrics |
| Strandness 設錯 | featureCounts 幾乎無 reads assigned | `-s` 或 library type 錯 | RSeQC infer_experiment.py |
| featureCounts no assignment | `Unassigned_NoFeatures` 高 | GTF/FASTA/BAM 不一致或 intronic reads | check annotation, strandedness, RNA type |
| Metadata 順序錯 | group signal 混亂 | count columns 未對齊 sample table | `identical(colnames(counts), metadata$sample_id)` |
| Count matrix 含小數 | DESeq2 報錯或 silent rounding | transcript estimated counts | 用 tximport 正確匯入或 round only when appropriate |
| TPM 直接跑 edgeR/DESeq2 | 結果模型假設錯 | TPM 不是 count | 回到 raw/estimated counts |
| Biological replicate 太少 | dispersion 不穩、power 低 | n 不足 | 增加 biological replicates |
| Group/batch confounded | design not full rank | 實驗安排完全重疊 | 無法統計修正，需新資料 |
| PCA outlier | 單一樣本遠離 | QC、batch、sample swap 或真實 biology | 多圖與 lab record 一起查 |
| Gene ID 無法轉換 | annotation 大量 NA | version suffix、物種 DB 錯 | 去 suffix、確認 OrgDb/biomaRt dataset |
| ORA background 錯 | pathway 過度顯著 | 用全基因組當 universe | 使用實際 tested genes |
| Technical replicate 當 biological | p-value 過小 | pseudo-replication | 合併 technical replicate 或正確建模 |

## What Was Verified Here

已實際執行：

```bash
MPLCONFIGDIR=/tmp/matplotlib-rnaseq \
python biology/genomics/sequencing-and-analysis/workflows/rna-seq/scripts/simulate_rnaseq_demo.py
```

已產生：

- `data/simulated_gene_counts.csv`
- `data/sample_metadata.csv`
- `data/simulated_library_qc.csv`
- `data/simulated_de_results.csv`
- `data/simulated_enrichment_results.csv`
- `src/*.png`

未在目前環境執行：

- Bash scripts：需要 FastQC、MultiQC、fastp、STAR、HISAT2、Salmon、kallisto、samtools、featureCounts 與真實 reference。
- R scripts：目前環境找不到 `Rscript`，且需要 Bioconductor packages。
- 真實 alignment/quantification：需要 reference FASTA/GTF/transcriptome 與足夠運算資源。

## Re-run Examples

```bash
cd /home/johnny_fan/project/notebook/biology/genomics/sequencing-and-analysis/workflows/rna-seq

# 重新產生本教學的模擬資料與圖。
MPLCONFIGDIR=/tmp/matplotlib-rnaseq python scripts/simulate_rnaseq_demo.py --outdir .

# 有真實 FASTQ 時。
bash scripts/fastq_qc.sh data/raw results/01_fastq_qc
bash scripts/fastp_trim.sh data/sample_metadata.csv . results/02_fastp_trim

# 有 reference 時。
THREADS=12 READ_LENGTH=101 bash scripts/star_alignment.sh reference/genome.fa reference/genes.gtf results/02_fastp_trim/fastq results/03_star
bash scripts/featurecounts_gene_counting.sh reference/genes.gtf results/03_star/bam results/06_featurecounts
```

後續可擴充方向：

- 加入真實公開資料集的 end-to-end 範例。
- 補 single-end、stranded/unstranded 三種 library 的對照結果。
- 加入 RSeQC gene body coverage 與 read distribution 實際圖。
- 加入 Salmon decoy-aware index 建立完整範例。
- 加入 batch correction、SVA/RUVSeq 與 time-course DE。
- 補充 transcript usage、alternative splicing 與 fusion analysis。

