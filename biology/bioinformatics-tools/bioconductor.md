[Biology](../README.md) › [生資工具](README.md) › Bioconductor

# Bioconductor 入門 (Introduction to Bioconductor)

Bioconductor 是 R 的基因體學套件生態系。它的價值不只是套件數量，而是一組**共用的資料結構**：序列、基因體區間、表現量矩陣都有標準物件，DESeq2、edgeR、limma、ChIP-seq 工具因此能互相銜接。R 基礎（vector / list、factor 參考組、join、匯入）見 [R Foundations](../../data-science/r-foundations/README.md)，特別是 [資料結構](../../data-science/r-foundations/data-structures.md) 與 [匯入資料](../../data-science/r-foundations/importing-data.md#生資檔案格式)。

> 本筆記的程式碼以 R 4.6.1 / Bioconductor 3.23（Biostrings 2.80、GenomicRanges 1.64、ShortRead 1.70、SummarizedExperiment 1.42）實跑驗證。

## 安裝

```r
install.packages("BiocManager")
BiocManager::install(c("Biostrings", "GenomicRanges", "ShortRead", "SummarizedExperiment"))
BiocManager::version()      # Bioconductor 版本與 R 版本綁定；不要混用 install.packages() 裝 Bioc 套件
BiocManager::valid()        # 檢查套件版本是否一致
```

## 核心物件

| 物件 | 套件 | 表示什麼 | 常用操作 |
| --- | --- | --- | --- |
| `DNAString` / `DNAStringSet` | Biostrings | 一條 / 多條序列（另有 RNA、AA 版本） | `reverseComplement()`、`translate()`、`letterFrequency()` |
| `IRanges` | IRanges | 整數區間（還沒有染色體） | `width()`、`shift()`、`reduce()` |
| `Rle` | S4Vectors | run-length 編碼的長向量 | `runLength()`、`runValue()` |
| `GRanges` | GenomicRanges | 基因體區間：染色體 + 區間 + 股別 + metadata | `findOverlaps()`、`subsetByOverlaps()`、`reduce()` |
| `ShortReadQ` | ShortRead | FASTQ reads 與品質 | `readFastq()`、`sread()`、`quality()`、`qa()` |
| `SummarizedExperiment` | SummarizedExperiment | 表現量矩陣 + 樣本資訊 + 特徵資訊 | `assay()`、`colData()`、`rowData()`、`rowRanges()` |

> 一律用 accessor（`seqnames()`、`assay()`），不要用 `@` 直接取 slot：內部結構隨版本變動，accessor 會維持相容。S4 物件概念見 [物件導向：S3 與 R6](../../data-science/r-foundations/object-oriented-programming-s3-r6.md)。

## 序列：Biostrings

```r
library(Biostrings)
dna <- DNAString("ATGATCTCGTAA")
reverseComplement(dna)                         # TTACGAGATCAT
translate(dna)                                 # MIS*
letterFrequency(dna, "GC", as.prob = TRUE)     # 0.333

genome <- readDNAStringSet("ref.fa")           # 多條序列（FASTA）
```

只是少量文字處理用一般字串即可；序列本身成為分析對象（反向互補、比對、計算組成）時再用 Biostrings。

## 區間：IRanges、Rle、GRanges

```r
library(GenomicRanges)

# 1. IRanges：width = end - start + 1（1-based、含頭尾）
IRanges(start = 20, end = 30)                       # width 11
IRanges(start = c(1, 20), width = c(30, 11))
IRanges(c(FALSE, FALSE, TRUE, TRUE, FALSE, TRUE))   # 邏輯向量 → TRUE 的連續區段：3-4、6-6

# 2. Rle：重複值很多的向量（染色體名、股別、覆蓋度）
Rle(c("chr1", "chr1", "chr1", "chr2"))              # lengths 3 1

# 3. GRanges：從字串或 data frame 建立
GRanges("chr1:200-300")
genes <- makeGRangesFromDataFrame(df, seqnames.field = "chrom",
                                  keep.extra.columns = TRUE)   # df 有 chrom、start、end、gene

# 4. 區間運算
peaks <- GRanges(c("chr1:120-130", "chr1:500-600"))
findOverlaps(peaks, genes)            # 哪個 peak 與哪個基因重疊（Hits 物件）
subsetByOverlaps(peaks, genes)        # 只留與基因重疊的 peak：chr1:120-130
reduce(c(genes, peaks))               # 合併重疊區間
```

> GRanges 是 **1-based、含頭尾**；BED 是 0-based、半開。`rtracklayer::import("x.bed")` 會自動轉換，自己用 `read.table()` 讀 BED 再建 GRanges 時，start 要 +1。見 [座標系統](../genomics/file-formats/zero-one-based.md)。

| bedtools | GenomicRanges |
| --- | --- |
| `intersect -u` | `subsetByOverlaps(a, b)` |
| `intersect -wa -wb` | `findOverlaps(a, b)` + 索引 |
| `merge` | `reduce()` |
| `subtract` | `setdiff()` |
| `closest` | `nearest()`、`distanceToNearest()` |
| `slop` | `resize()`、`flank()`、`a + 100` |

命令列版本見 [bedtools](ngs-tools/bedtools.md)。

## Reads：ShortRead

```r
library(ShortRead)

fq <- readFastq("data", pattern = "fastq.gz")       # 整個讀進記憶體
sampler <- FastqSampler("data/sample.fastq.gz", n = 1e5)
sub <- yield(sampler); close(sampler)               # 大檔先隨機抽樣

sread(fq)[1]                                        # 序列（DNAStringSet）
quality(fq)[1]                                      # ASCII 品質字串
qs <- as(PhredQuality(quality(quality(fq))), "IntegerList")   # 轉成數值 Phred 分數
qs[[1]][1:4]                                        # 40 40 20 2（'I' '5' '#' 的 Phred+33）

abc <- alphabetByCycle(sread(fq))                   # 每個 cycle 的 A/C/G/T 計數（看組成偏差）
qa_res <- qa(fq, lane = "1")                        # QC 摘要：readCounts、baseQuality、perCycle、
report(qa_res)                                      # frequentSequences、adapterContamination… 產生 HTML
```

ASCII 品質編碼與 Phred 換算見 [鹼基品質分數](../genomics/ngs-qc/base-quality-scores.md)。實務上 FASTQ QC 多用命令列的 [FastQC](ngs-tools/fastqc.md) / [fastp](ngs-tools/fastp.md)；ShortRead 適合在 R 裡做客製化檢查。

## 表現量矩陣：SummarizedExperiment

RNA-seq、甲基化、蛋白質體的「特徵 × 樣本」矩陣，加上樣本資訊與特徵資訊，打包成一個物件；**切子集時三者自動同步**，不會發生 metadata 與欄位錯位。

```
              colData（樣本：cell、dex、batch…）
              ┌───────────────┐
 rowData /    │  assay(se)    │   counts、log-CPM 等，可存多個 assay
 rowRanges    │  基因 × 樣本  │
 （基因資訊）  └───────────────┘
```

```r
library(SummarizedExperiment)
data(airway, package = "airway")      # 氣道平滑肌細胞 ± dexamethasone 的 RNA-seq
airway                                # dim: 63677 8；assays: counts
assay(airway, "counts")[1:3, 1:3]
colData(airway)[, c("cell", "dex")]   # 樣本資訊
rowRanges(airway)                     # 每個基因的 exon 位置（GRangesList）

trt <- airway[, airway$dex == "trt"]  # 63677 × 4，colData 同步切
expressed <- airway[rowSums(assay(airway)) > 0, ]

# 自己建
se <- SummarizedExperiment(assays = list(counts = count_mat),
                           colData = sample_info, rowData = gene_info)
```

`DESeqDataSet`（DESeq2）是 SummarizedExperiment 的子類別；單細胞的 `SingleCellExperiment` 也是。Python 的對應是 [AnnData](../../data-science/python-foundations/anndata-and-scanpy.md)。下游分析見 [RNA-seq 分析](../genomics/workflows/rna-seq/README.md)。

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 把 Bioconductor 套件當成獨立工具，各自轉成 data frame | 盡量在 GRanges / SummarizedExperiment 中完成運算，最後才轉出 |
| 座標長期存成 data frame，手寫重疊判斷 | 轉成 GRanges 用 `findOverlaps()` |
| `seqnames` 不一致（`chr1` vs `1`）導致重疊結果為空 | `library(GenomeInfoDb)` 後 `seqlevelsStyle(gr) <- "UCSC"`（Bioc 3.22 起 GenomicRanges 改依賴輕量的 Seqinfo，這個函式要另外載入 GenomeInfoDb） |
| 大型 FASTQ 一次讀入記憶體 | `FastqSampler` 抽樣或 `FastqStreamer` 分批讀 |
| 樣本資訊與 count 矩陣分開存，排序不一致 | 包成 SummarizedExperiment，並檢查 `all(colnames(counts) == rownames(sample_info))` |
| 用 `install.packages()` 裝 Bioc 套件或混用版本 | 一律 `BiocManager::install()`，`BiocManager::valid()` 檢查 |
