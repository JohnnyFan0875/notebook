[基因體學](../README.md) › [檔案格式](README.md) › FASTQ

# FASTQ

定序儀輸出的標準格式：每條 read 存序列與每個鹼基的品質分數，是比對、定量、變異呼叫的起點。

## 結構：每條 read 4 行

```text
@A00123:45:HXXXXXXX:1:1101:10000:1000 1:N:0:ACGTACGT
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCAC
+
FFFFFFFFF:FFFFFFFFFFFFFFFFF,FFFFFFFFF:FFFFFFFFFFF:FF#FF
```

| 行 | 內容 |
| --- | --- |
| 1 | `@` + read 名稱（Illumina：儀器 : run : flow cell : lane : tile : x : y）+ 空白 + `讀序 : 是否被過濾 : 控制碼 : index 序列` |
| 2 | 序列 |
| 3 | `+`（可重複名稱，現在多留空） |
| 4 | 品質字串，**長度必須與序列相同**；字元 ASCII 碼 − 33 = Phred 分數 |

品質編碼、Q30、分箱見 [鹼基品質分數](../ngs-qc/base-quality-scores.md)。

## 成對 (paired-end) 與檔名

| 項目 | 說明 |
| --- | --- |
| R1 / R2 | 同一個片段的兩端，分在兩個檔案：`S1_L001_R1_001.fastq.gz`、`S1_L001_R2_001.fastq.gz` |
| 同步 | 兩個檔案的 reads 順序必須一一對應；只修剪其中一個檔案會破壞配對（fastp 等工具會同時處理） |
| I1 / I2 | index（barcode）reads；多數情況已 demultiplex，不需要 |
| 多個 lane | 同一樣本的 `L001`–`L004` 可直接 `cat` 合併（gzip 可串接），或分別比對後合併 BAM |
| interleaved | R1、R2 交錯存在同一檔案（較少見） |

## 常用操作

```bash
zcat S1_R1.fastq.gz | head -8                        # 看前兩條 read
echo $(( $(zcat S1_R1.fastq.gz | wc -l) / 4 ))        # reads 數
seqkit stats *.fastq.gz                               # reads 數、長度分布、Q30 比例（-a）
seqkit sample -p 0.1 -s 42 S1_R1.fastq.gz -o sub.fq.gz   # 抽 10%（R1、R2 用同一個 seed）
```

公開資料（SRA / ENA）的下載見 [原始資料庫](../reference-data/raw-data-repositories.md)。

## 品質控制

| 工具 | 用途 |
| --- | --- |
| [FastQC](../../bioinformatics-tools/ngs-tools/fastqc.md) + MultiQC | 品質報告 |
| [fastp](../../bioinformatics-tools/ngs-tools/fastp.md) | 修剪 adapter / 低品質、過濾 |
