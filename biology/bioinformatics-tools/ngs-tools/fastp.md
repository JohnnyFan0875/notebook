[生資工具](../README.md) › [NGS 工具](README.md) › fastp

# fastp

一步完成 FASTQ 前處理：adapter 修剪、品質過濾、polyG 修剪、成對 reads 校正、UMI 處理，並輸出 HTML / JSON 報告。速度快、多數參數有合理預設，是目前最常用的修剪工具之一。

## 用法

```bash
conda install -c bioconda fastp

# 成對 (paired-end)
fastp -i S1_R1.fastq.gz -I S1_R2.fastq.gz \
      -o S1_R1.clean.fq.gz -O S1_R2.clean.fq.gz \
      --detect_adapter_for_pe \
      -w 8 -h S1.fastp.html -j S1.fastp.json

# 單端 (single-end)
fastp -i S1.fastq.gz -o S1.clean.fq.gz -w 8 -h S1.fastp.html -j S1.fastp.json
```

## 常用參數

| 參數 | 預設 | 意義 |
| --- | --- | --- |
| `--detect_adapter_for_pe` | 關 | 成對資料也做 adapter 序列偵測（預設只靠 R1/R2 重疊判斷） |
| `-a SEQ` | 自動 | 指定 adapter 序列 |
| `-q` / `-u` | 15 / 40 | 品質 < `-q` 的鹼基視為不合格；不合格比例 > `-u`% 的 read 丟棄 |
| `-l` | 15 | 修剪後短於此長度的 read 丟棄 |
| `--cut_front` / `--cut_tail` | 關 | 滑動視窗從 5′ / 3′ 修剪低品質尾端 |
| `--trim_poly_g` | NextSeq / NovaSeq 自動開 | 2-color 化學無訊號會讀成 G，產生假的 polyG 尾巴 |
| `-c` | 關 | 成對 reads 重疊區的鹼基互相校正 |
| `--dedup` | 關 | 去除完全相同的 reads（一般不建議在比對前做） |
| `-U --umi_loc read1 --umi_len 8` | 關 | 把 UMI 從序列移到 read 名稱，供下游依 UMI 去重 |
| `-w` | 3 | 執行緒數 |

> polyG 的成因見 [Illumina 2-color 化學](../../genomics/sequencing-techniques/illumina-color-chemistry.md)。

## 報告重點

| 項目 | 看什麼 |
| --- | --- |
| Filtering result | 通過 / 因低品質 / 太短 / N 太多被丟棄的 reads 比例；丟棄 > 10% 要找原因 |
| Duplication | 估計重複率（未比對前的粗估） |
| Insert size | 由成對重疊推估的片段長度 |
| Adapter | 偵測到的 adapter 序列與修剪的鹼基數 |
| Before / after filtering | 品質、GC、鹼基組成在過濾前後的比較 |

JSON 報告可交給 MultiQC 彙整多樣本。

## 什麼時候不要過度修剪

| 情境 | 建議 |
| --- | --- |
| RNA-seq 用 STAR / Salmon | 只修 adapter 即可；比對器會 soft-clip 低品質尾端，過度修剪反而損失資訊 |
| 變異呼叫 | 品質修剪溫和即可；GATK 會用鹼基品質加權，BQSR 會校正 |
| amplicon panel | primer 序列要另外修掉（cutadapt 或專用工具），否則會遮蔽 primer 區的真實變異 |
| small RNA | 要明確指定 adapter，並調低 `-l` |

替代工具：Trim Galore（cutadapt 包裝）、Trimmomatic、cutadapt。官方：[fastp GitHub](https://github.com/OpenGene/fastp)。
