[基因體學](../README.md) › [檔案格式](README.md) › 座標系統

# 座標系統：0-based vs 1-based (Coordinate Systems)

不同格式與工具對「第一個鹼基是 0 還是 1」、「終點含不含」的約定不同，差一個鹼基 (off-by-one) 是註解錯誤最常見的來源。

## 兩種系統

```
序列:        A   C   G   T   A
1-based:     1   2   3   4   5        「第 2–4 個鹼基」= 2-4（含頭尾）
0-based:   0   1   2   3   4   5      「第 2–4 個鹼基」= [1, 4)（含起點、不含終點）
```

| 系統 | 單一鹼基（第 101 個） | 區間（第 101–200 個） | 長度 |
| --- | --- | --- | --- |
| 1-based 閉區間 | `101` 或 `101-101` | `101-200` | end − start + 1 |
| 0-based 半開區間 | `100-101` | `100-200` | end − start |

**轉換**：1-based → 0-based 半開：start − 1、end 不變；反向：start + 1、end 不變。

## 各格式 / 工具的約定

| 0-based 半開 | 1-based 閉區間 |
| --- | --- |
| [BED](bed.md)、bigBed、bedGraph | [VCF](vcf.md)、[SAM](bam.md)（POS）、[GTF / GFF](gtf-gff.md) |
| BAM 內部的二進位欄位 | HGVS 命名（`c.68_69del`）、Ensembl / NCBI 網站 |
| UCSC 資料庫表格（`*.txt.gz`） | UCSC Genome Browser 網頁顯示 |
| Python 切片 `seq[100:200]`、pysam、pyBigWig | R、Bioconductor（`GRanges`、`IRanges`） |
| sambamba depth 輸出 | samtools depth / `samtools faidx ref.fa chr1:101-200` |

> **UCSC 的陷阱**：網頁上顯示 1-based，但下載的資料表與 BED 是 0-based。從 Table Browser 存出的區間與網頁上看到的起點差 1。

## 範例

| 描述 | VCF / 網頁（1-based） | BED（0-based） |
| --- | --- | --- |
| chr7 第 140,753,336 個鹼基的 SNV | `chr7  140753336` | `chr7  140753335  140753336` |
| 一段 exon：第 1,001–1,050 個鹼基 | `chr1:1001-1050` | `chr1  1000  1050` |
| 插入位點（兩個鹼基之間） | 以前一個鹼基表示 | 長度 0 的區間：`chr1  1000  1000` |

## 常見錯誤

| 錯誤 | 後果 | 避免方式 |
| --- | --- | --- |
| VCF 位置直接當 BED 起點 | 區間往右偏 1 | BED 起點 = POS − 1 |
| 自己用 `read.table()` 讀 BED 建 GRanges | 起點差 1 | 用 `rtracklayer::import()`，或 start + 1 |
| Python 切片當 1-based | 少取或多取一個鹼基 | 記住切片是 0-based 半開 |
| 不同基因體版本混用 | 差幾千到幾百萬個鹼基，不只 1 | 檢查 hg19 / hg38，見 [參考基因組](../reference-data/reference-genomes.md) |

bedtools、bcftools 讀不同格式時會自動處理；手動轉檔或寫程式時最容易出錯。參考：[One-based vs zero-based](https://qinqianshan.com/biology/bioknowledge/one-based-and-zero-based/)、[UCSC 說明](https://genome-blog.gi.ucsc.edu/blog/2016/12/12/the-ucsc-genome-browser-coordinate-counting-systems/)。
