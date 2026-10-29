[基因體學](../README.md) › [檔案格式](README.md) › BED

# BED (Browser Extensible Data)

描述基因體區間的純文字格式：目標區域 (panel targets)、exon、ChIP-seq peak、低覆蓋區域都用 BED。座標是 **0-based、半開區間** `[start, end)`，見 [座標系統](zero-one-based.md)。

```text
chr1    1    2       # 第 2 個鹼基（1-based）
chr1    1    1000    # 第 2–1000 個鹼基，長度 999
```

## 欄位

前 3 欄必填（BED3），其餘依序選填，最多 12 欄（BED12）。

| # | 欄位 | 意義 | 例 |
| --- | --- | --- | --- |
| 1 | chrom | 染色體 | `chr1` |
| 2 | chromStart | 起點（0-based，含） | `999` |
| 3 | chromEnd | 終點（不含） | `1050` |
| 4 | name | 名稱 | `geneA` |
| 5 | score | 0–1000（瀏覽器用來調深淺） | `960` |
| 6 | strand | `+`、`-`、`.` | `+` |
| 7–8 | thickStart / thickEnd | 粗線顯示範圍（如 CDS） | `1000`、`1045` |
| 9 | itemRgb | 顏色 `R,G,B` | `0,0,255` |
| 10 | blockCount | 區塊數（如 exon 數） | `2` |
| 11 | blockSizes | 各區塊長度 | `20,30` |
| 12 | blockStarts | 各區塊相對 chromStart 的起點 | `0,21` |

```text
chr1  999  1050  geneA  960  +  1000  1045  0,0,255  2  20,30  0,21
```

這筆代表兩個 exon：[999, 1019) 與 [1020, 1050)，對應 1-based 的 1000–1019 與 1021–1050。

## 相關格式

| 格式 | 用途 |
| --- | --- |
| BED6 + 自訂欄 | 很多工具輸出「BED 前 6 欄 + 額外欄位」（如 narrowPeak：ChIP-seq peak） |
| bedGraph | `chrom start end value`，連續訊號（覆蓋度） |
| bigBed / bigWig | BED / bedGraph 的二進位索引版，適合大檔與瀏覽器遠端讀取（`bedToBigBed`、`bedGraphToBigWig`） |
| interval_list | Picard / GATK 的區間格式（1-based，含 header），用 `picard BedToIntervalList` 轉換 |

## 用途與注意

| 用途 | 注意 |
| --- | --- |
| 限定分析區域（BAM / VCF） | 染色體命名與基因體版本要一致 |
| panel 目標與 padding | 合併重疊區間再加 padding，見 [bedtools](../../bioinformatics-tools/ngs-tools/bedtools.md#範例panel-目標區域整理) |
| 瀏覽器軌道 | 可加 `track name=... color=...` header 行 |
| 排序 | 多數工具要求 `sort -k1,1 -k2,2n` 排序 |

工具：[bedtools](../../bioinformatics-tools/ngs-tools/bedtools.md)、[IGV](../../bioinformatics-tools/visualization/igv.md)、[samtools view -L](../../bioinformatics-tools/ngs-tools/samtools.md)、GenomicRanges（R，讀入時自動轉成 1-based）。規格：[UCSC BED 格式](https://genome.ucsc.edu/FAQ/FAQformat.html#format1)。
