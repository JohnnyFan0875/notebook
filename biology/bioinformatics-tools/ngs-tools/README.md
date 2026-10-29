[Biology](../../README.md) › [生資工具](../README.md) › NGS 工具

# NGS 工具 (NGS Command-Line Tools)

處理 FASTQ、BAM、VCF、BED 的命令列工具，依任務整理。多數可用 `conda install -c bioconda <tool>` 或 Docker（BioContainers）安裝，見 [conda](../../../computing/containers-and-env/conda.md)。

## 想做 X → 用哪個

| 任務 | 工具 | 指令 |
| --- | --- | --- |
| FASTQ 品質報告 | [FastQC](fastqc.md) + MultiQC | `fastqc *.fastq.gz -o qc/` → `multiqc qc/` |
| 修剪 adapter、低品質尾端 | [fastp](fastp.md) | `fastp -i R1 -I R2 -o out1 -O out2` |
| BAM 排序、索引、統計 | [samtools](samtools.md) | `samtools sort`、`index`、`flagstat`、`stats` |
| 取出某區域的 reads | [samtools](samtools.md) | `samtools view -b in.bam chr1:1-1000` |
| 標記 PCR / 光學重複 | [Picard MarkDuplicates](picard-markduplicates.md)、`samtools markdup`、`sambamba markdup` | 見各筆記 |
| 每個鹼基 / 每個區域的深度 | [samtools](samtools.md)、[sambamba](sambamba.md) | `samtools depth`、`sambamba depth base / region` |
| VCF 過濾、拆分多等位、加註解 | [bcftools](bcftools.md) | `bcftools filter`、`norm`、`annotate` |
| 壓縮並索引 VCF / BED / GFF | [tabix](tabix.md) | `bgzip` + `tabix -p vcf` |
| 區間交集、合併、覆蓋度 | [bedtools](bedtools.md) | `bedtools intersect`、`merge`、`coverage` |
| 標記重複序列 | [RepeatMasker](repeatmasker.md) | `RepeatMasker -species human` |
| 目視檢查 | [IGV](../visualization/igv.md) | — |

## 工具比較

| 工具 | 處理的檔案 | 強項 | 替代方案 |
| --- | --- | --- | --- |
| [FastQC](fastqc.md) | FASTQ / BAM | 標準 QC 報告 | fastp 內建報告、`seqkit stats` |
| [fastp](fastp.md) | FASTQ | 一步完成修剪 + 過濾 + 報告，速度快 | Trim Galore、Trimmomatic、cutadapt |
| [samtools](samtools.md) | SAM / BAM / CRAM | 標準、功能最全 | sambamba |
| [Picard](picard-markduplicates.md) | BAM | GATK 流程標準、重複指標完整 | `samtools markdup`、sambamba |
| [sambamba](sambamba.md) | BAM | 多執行緒、深度計算附鹼基組成 | samtools、mosdepth（深度最快） |
| [bcftools](bcftools.md) | VCF / BCF | 過濾、正規化、合併、查詢 | GATK `SelectVariants`、vcftools |
| [tabix](tabix.md) | 排序過的 bgzip 文字檔 | 依座標快速查詢 | `bcftools index` |
| [bedtools](bedtools.md) | BED / GFF / VCF / BAM | 區間運算 | GenomicRanges（R）、pybedtools、bedops |
| [RepeatMasker](repeatmasker.md) | FASTA | 重複序列標記 | 直接下載 UCSC `rmsk` 軌道 |

> 跨工具最常見的錯誤：**染色體命名不一致**（`chr1` vs `1` vs `NC_000001.11`）與**基因體版本不一致**（GRCh37 vs GRCh38）。比對、註解、BED 與 VCF 必須用同一個 reference，見 [座標系統](../../genomics/file-formats/zero-one-based.md)。
