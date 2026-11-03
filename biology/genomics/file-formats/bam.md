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

CIGAR 描述比對的**結構**：由左到右，哪裡比對上、哪裡插入 / 缺失、哪裡被 clip。

| 操作 | 意義 | 消耗 read | 消耗參考 |
| --- | --- | --- | --- |
| `M` | 比對（相同或錯配都算） | ✓ | ✓ |
| `=` / `X` | 相同 / 錯配（較少使用） | ✓ | ✓ |
| `I` | 插入（read 多出的鹼基） | ✓ | |
| `D` | 缺失（read 少了的鹼基） | | ✓ |
| `N` | 跳過參考（RNA-seq 的 intron） | | ✓ |
| `S` | soft clip（序列保留但沒比對） | ✓ | |
| `H` | hard clip（序列已移除） | | |
| `P` | padding（很少用） | | |

例：`76M2I22M1D1M` = 76 個比對、2 個插入、22 個比對、1 個缺失、1 個比對；read 長 76 + 2 + 22 + 1 = 101，跨越參考 76 + 22 + 1 + 1 = 100 bp。RNA-seq 的 `50M2000N51M` 代表跨越 2,000 bp 的 intron。大量 soft clip 常是 adapter 殘留或結構變異斷點。

> 預設的 `M` 不區分相同與錯配，所以**光看 CIGAR 看不出 SNV**。

![CIGAR 示意](https://ugc.futurelearn.com/uploads/assets/f8/31/f8314226-810d-4b91-bdbf-05be43f1ca37.png)

<sub>圖片來源：[FutureLearn](https://www.futurelearn.com/info/courses/bioinformatics-for-biologists-analysing-and-interpreting-genomics-datasets/0/steps/388425)</sub>

## MD 與 NM：錯配與編輯距離

| 標籤 | 格式 | 內容 |
| --- | --- | --- |
| `MD` | `MD:Z:...` | 比對區內哪些位置與參考不同，以及**參考在那裡是什麼鹼基**；不需參考 FASTA 就能重建參考序列 |
| `NM` | `NM:i:n` | 編輯距離 (edit distance) = 錯配數 + 插入鹼基數 + 缺失鹼基數 |

| MD 元素 | 意義 |
| --- | --- |
| 數字 | 連續相同的鹼基數 |
| 單一字母 | 錯配，字母是**參考**鹼基（read 變成什麼要回頭看 SEQ） |
| `^` + 字母 | 缺失，後面接被刪掉的參考鹼基 |
| `0` | 兩個相鄰錯配 / 缺失之間的分隔（如 `2G0G0^AT4`） |

MD 沿**參考序列**走，所以 **soft clip 與插入不會出現在 MD**，插入前後的相同數會合併成一個數字；判讀時要搭配 CIGAR。

### 完整範例

```text
參考（chr1:1001 起，24 bp）：ACGTACGTACGGATTCAGCTAAGC
Read（27 bp）             ：TTAACGTACGTGCGGTTATTCCTAAGC

去掉開頭 3 bp soft clip 後：
Ref : ACGTACGTACGG--ATTCAGCTAAGC
Read: ACGTACGTGCGGTTATTC--CTAAGC
              ^     ^^    ^^
            錯配   插入  缺失

read1  0  chr1  1001  60  3S12M2I4M2D6M  *  0  0  TTAACGTACGTGCGGTTATTCCTAAGC  IIII...  NM:i:5  MD:Z:8A7^AG6
```

| 片段 | CIGAR | MD | 說明 |
| --- | --- | --- | --- |
| `TTA` | `3S` | — | soft clip，MD 不記錄 |
| 參考 1–12 | `12M` | `8` `A` `3…` | 第 9 位錯配：參考 A、read G；CIGAR 仍寫 `M` |
| `TT` | `2I` | — | 插入，MD 看不到 |
| 參考 13–16 | `4M` | `…4` | 與前面錯配後的 3 個相同合併成 `7` |
| 參考 17–18 | `2D` | `^AG` | 參考的 `AG` 在 read 缺失 |
| 參考 19–24 | `6M` | `6` | |

驗算：read 長 3 + 12 + 2 + 4 + 6 = 27；參考長 12 + 4 + 2 + 6 = 24 = MD 8 + 1 + 7 + 2 + 6；NM = 1 錯配 + 2 插入 + 2 缺失 = 5。

### 只有 CIGAR 能看出什麼

| 變異 | 只有 CIGAR + SEQ | 加上 MD 或參考 FASTA |
| --- | --- | --- |
| 插入 | `I`，位置與序列都在 SEQ | — |
| 缺失 | `D`，知道位置與長度，**不知道被刪的鹼基** | `^` 後的參考鹼基 |
| SNV | 藏在 `M` 裡，**完全看不出** | 參考鹼基 (ref)；SEQ 是 read 鹼基 (alt) |
| delins | 沒有專屬符號，拆成 `M` / `I` / `D` 組合 | 可還原 |

例：參考 `ACGGATTCAG`、read `ACCCTCAG`（`GGAT` → `CC`），比對器可能給 `4M2D4M`，看不出前 4 個 `M` 中第 3、4 位是錯配；MD 為 `MD:Z:2G0G0^AT4`。

> 分工：**SEQ = 變成什麼 (alt)**、**參考或 MD = 原本是什麼 (ref)**、**CIGAR = 位置對應**、QUAL = 這個鹼基可不可信。MD / NM 只是方便快速判讀，沒有它們仍可用 SEQ + CIGAR + 參考完整重算。同一個 delins 可能有多種 CIGAR 寫法，BAM 裡的是比對器的解讀，所以變異呼叫常需要 realignment 與左對齊（見 [VCF：同一個變異的不同寫法](vcf.md#同一個變異的不同寫法)）。

### 各比對器是否輸出 MD

| 比對器 | 預設 | 要加的參數 |
| --- | --- | --- |
| BWA-MEM / aln | 輸出 NM、MD | — |
| Bowtie2 | 輸出 NM、MD | — |
| minimap2 | 輸出 NM，**不輸出 MD** | `--MD`；另有 `--eqx`（CIGAR 用 `=` / `X`）、`--cs`（cs tag，合併 CIGAR 與 MD 並含 read 鹼基） |
| STAR | 只有 `NH HI AS nM` | `--outSAMattributes NH HI AS nM NM MD` |
| HISAT2 | 通常有 NM、MD | 以實際檔案為準 |

預設值可能隨版本變動；看 header 的 `@PG` 可知 BAM 用哪個工具與參數產生。CRAM 以「相對參考的差異」存序列，通常不存 MD / NM，解碼時再由參考重建。

```bash
samtools view aln.bam | head -n 3              # 第 12 欄之後是 tag
samtools view aln.bam | grep -c "MD:Z:"        # 有 MD 的 read 數
samtools view -d MD aln.bam | head             # 只輸出帶 MD 的 read
samtools calmd -b aln.bam ref.fa > aln.md.bam  # 補上 MD / NM（需同一份參考）
```

常見用途：依 NM 過濾差異過大的 read、統計錯配 / indel 率以比較定序平台（見 [定序平台：短讀化學](../sequencing-techniques/sequencing-platforms.md#短讀平台的擴增與定序化學illuminamgielement)）、不載入參考就快速判讀 pileup。IGV 不需要 MD，直接用參考比對顯示，見 [IGV](../../bioinformatics-tools/visualization/igv.md#變異怎麼顯示)。

## 工具

| 工具 | 用途 |
| --- | --- |
| [samtools](../../bioinformatics-tools/ngs-tools/samtools.md) | 檢視、排序、索引、過濾、統計 |
| [Picard](../../bioinformatics-tools/ngs-tools/picard-markduplicates.md) | 標記重複、收集指標 |
| [bedtools](../../bioinformatics-tools/ngs-tools/bedtools.md) | 與 BED 區間交集、計算覆蓋度 |
| [IGV](../../bioinformatics-tools/visualization/igv.md) | 目視檢查 |
| pysam（Python）、Rsamtools / GenomicAlignments（R） | 程式化讀取 |

中文說明：[SAM、BAM 與 CRAM（weitinglin）](https://weitinglin.com/2016/01/27/sambam-and-cram/)、[BAM 格式（yourgene）](https://yourgene.pixnet.net/blog/post/95204728)。
