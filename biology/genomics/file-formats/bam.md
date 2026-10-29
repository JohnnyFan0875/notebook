[基因體學](../README.md) › [檔案格式](README.md) › SAM / BAM / CRAM

# SAM / BAM / CRAM

儲存 reads 比對到參考基因組的結果。SAM 是純文字；BAM 是 BGZF 壓縮的二進位版本（可建索引隨機存取）；CRAM 以參考序列為基礎壓縮，檔案再小約 40–60%，但讀取時需要**同一份參考 FASTA**。

## 結構

```text
@HD  VN:1.6  SO:coordinate
@SQ  SN:chr1  LN:248956422
@RG  ID:HXXXXXXX.1  SM:sample1  PL:ILLUMINA  LB:lib1
@PG  ID:bwa  PN:bwa  VN:0.7.17  CL:bwa mem -R ... GRCh38.fa R1.fq.gz R2.fq.gz
A00123:45:HXXXXXXX:1:1101:10000:1000  99  chr1  10050  60  101M  =  10250  301  AGCTTAGC...  FFFFFFFF...  NM:i:1  MD:Z:50A50  RG:Z:HXXXXXXX.1
```

| Header | 內容 |
| --- | --- |
| `@HD` | 格式版本、排序方式（`SO:coordinate` / `queryname` / `unsorted`） |
| `@SQ` | 參考序列名稱與長度：**可用來確認 hg19 / hg38 與 chr 命名** |
| `@RG` | read group：`SM`（樣本）、`LB`（library）、`PL`（平台）、`ID`；GATK 必需 |
| `@PG` | 處理過的程式與指令，追溯流程 |

## 比對紀錄的 11 個必要欄位

| # | 欄位 | 意義 | 例 |
| --- | --- | --- | --- |
| 1 | QNAME | read 名稱 | `A00123:...:1000` |
| 2 | FLAG | 位元旗標（見下） | `99` |
| 3 | RNAME | 參考序列名稱 | `chr1` |
| 4 | POS | 最左端比對位置（**1-based**） | `10050` |
| 5 | MAPQ | 比對品質（見 [比對品質](../ngs-qc/mapping-quality.md)） | `60` |
| 6 | CIGAR | 比對型態（見下） | `101M` |
| 7 | RNEXT | mate 的參考序列（`=` 同一條、`*` 無） | `=` |
| 8 | PNEXT | mate 的位置 | `10250` |
| 9 | TLEN | 片段長度 (template length)；正負代表左右 | `301` |
| 10 | SEQ | read 序列（依參考序列正股方向） | |
| 11 | QUAL | 品質字串 | |
| 12+ | 選填標籤 | `NM`（編輯距離）、`MD`（錯配位置）、`RG`、`AS`（比對分數）、`XS`（次佳分數） | |

## FLAG：位元加總

| 位元 | 十進位 | 意義 |
| --- | --- | --- |
| 0x1 | 1 | 成對定序 |
| 0x2 | 2 | 正確配對 (proper pair) |
| 0x4 | 4 | 本身未比對 |
| 0x8 | 8 | mate 未比對 |
| 0x10 | 16 | 反向股 |
| 0x20 | 32 | mate 在反向股 |
| 0x40 / 0x80 | 64 / 128 | R1 / R2 |
| 0x100 | 256 | 次要比對 (secondary) |
| 0x200 | 512 | 未通過 QC |
| 0x400 | 1024 | PCR / 光學重複 |
| 0x800 | 2048 | 補充比對 (supplementary) |

例：`99` = 64 + 32 + 2 + 1 → R1、mate 在反向股、正確配對、成對；`147` = 128 + 16 + 2 + 1 → 它的 R2。可用 [Explain SAM Flags](https://broadinstitute.github.io/picard/explain-flags.html) 查詢。常用過濾：`samtools view -F 0x904`（排除未比對、次要、補充比對）。

## CIGAR

| 操作 | 意義 | 消耗 read | 消耗參考 |
| --- | --- | --- | --- |
| `M` | 比對（相同或錯配都算） | ✓ | ✓ |
| `=` / `X` | 相同 / 錯配（較少使用） | ✓ | ✓ |
| `I` | 插入（read 多出的鹼基） | ✓ | |
| `D` | 缺失（read 少了的鹼基） | | ✓ |
| `N` | 跳過參考（RNA-seq 的 intron） | | ✓ |
| `S` | soft clip（序列保留但沒比對） | ✓ | |
| `H` | hard clip（序列已移除） | | |

例：`76M2I23M1D` = 76 個比對、2 個插入、23 個比對、1 個缺失；read 長 76 + 2 + 23 = 101，跨越參考 76 + 23 + 1 = 100 bp。RNA-seq 的 `50M2000N51M` 代表跨越 2,000 bp 的 intron。大量 soft clip 常是 adapter 殘留或結構變異斷點。

![CIGAR 示意](https://ugc.futurelearn.com/uploads/assets/f8/31/f8314226-810d-4b91-bdbf-05be43f1ca37.png)

<sub>圖片來源：[FutureLearn](https://www.futurelearn.com/info/courses/bioinformatics-for-biologists-analysing-and-interpreting-genomics-datasets/0/steps/388425)</sub>

## 工具

| 工具 | 用途 |
| --- | --- |
| [samtools](../../bioinformatics-tools/ngs-tools/samtools.md) | 檢視、排序、索引、過濾、統計 |
| [Picard](../../bioinformatics-tools/ngs-tools/picard-markduplicates.md) | 標記重複、收集指標 |
| [bedtools](../../bioinformatics-tools/ngs-tools/bedtools.md) | 與 BED 區間交集、計算覆蓋度 |
| [IGV](../../bioinformatics-tools/visualization/igv.md) | 目視檢查 |
| pysam（Python）、Rsamtools / GenomicAlignments（R） | 程式化讀取 |

中文說明：[SAM、BAM 與 CRAM（weitinglin）](https://weitinglin.com/2016/01/27/sambam-and-cram/)、[BAM 格式（yourgene）](https://yourgene.pixnet.net/blog/post/95204728)。
