[基因體學](../README.md) › [NGS 品質指標](README.md) › 比對品質

# 比對品質 (Mapping Quality, MAPQ)

MAPQ 是比對器對「這條 read 放在這個位置是錯的」的機率估計，存在 [BAM](../file-formats/bam.md) 第 5 欄。它和 [鹼基品質](base-quality-scores.md) 不同：鹼基品質問「這個鹼基讀對了嗎」，MAPQ 問「這條 read 放對地方了嗎」。

$$\text{MAPQ} = -10\log_{10} P(\text{位置錯誤})$$

MAPQ 低的主因是 read 能同樣好地對到多個位置：重複序列、假基因 (pseudogene)、片段重複 (segmental duplication)、同源基因家族。

## 各比對器的數值意義

公式相同，但各比對器的實際刻度不同，**不能跨工具比較同一個閾值**。

| 比對器 | 範圍 | 關鍵數值 |
| --- | --- | --- |
| BWA-MEM | 0–60 | 60 = 唯一比對；0 = 多個位置一樣好 |
| Bowtie2 | 0–42 | 42 = 唯一；0–1 = 多重比對 |
| STAR | 255 / 3 / 1 / 0 | 255 = 唯一；3 = 2 個位置；1 = 3–4 個；0 = > 4 個 |
| HISAT2 | 60 / 1 / 0 | 60 = 唯一；1 = 多重；0 = 非常多 |
| minimap2 | 0–60 | 長讀；與 BWA 類似 |

> STAR 的 255 不是「品質最高的 255 分」，只是「唯一比對」的標記；對 STAR 的 BAM 用 `-q 20` 等於只留唯一比對（其他值都 ≤ 3）。過濾前先確認比對器的刻度。

## 過濾

```bash
samtools view -b -q 20 in.bam > mapq20.bam           # MAPQ ≥ 20
samtools view -c -q 1 in.bam                          # MAPQ ≥ 1 的 reads 數（排除 MAPQ 0）
```

| 用途 | 常見做法 |
| --- | --- |
| Germline 變異呼叫 | GATK 預設忽略 MAPQ < 20 的 reads（`MappingQualityReadFilter`） |
| 體細胞 / 低頻變異 | 常用 MAPQ ≥ 20–30，並排除重複區的候選 |
| RNA-seq 計數 | featureCounts 預設不計多重比對（加 `-M` 才計入）；Salmon 以 EM 演算法分配多重比對 |
| ChIP-seq / ATAC-seq | MAPQ ≥ 30，並套用 ENCODE blacklist |
| 深度計算 | sambamba 預設排除 MAPQ 0（見 [sambamba](../../bioinformatics-tools/ngs-tools/sambamba.md)） |

## 判讀

| 現象 | 可能原因 |
| --- | --- |
| MAPQ 0 比例高 | 重複區多（如著絲點附近）、read 太短、參考基因體含 alt contig 卻未用 alt-aware 比對 |
| 某基因的變異只出現在 MAPQ 低的 reads | 假基因干擾（例：*PMS2* / *PMS2CL*、*SMN1* / *SMN2*、*CYP2D6* / *CYP2D7*） |
| 變異的 MAPQ（VCF 的 `MQ`）偏低 | 偽陽性風險高，VQSR 與硬過濾都會參考 `MQ`、`MQRankSum`（見 [VQSR](vqsr.md)） |

> 臨床上，低 MAPQ 區域（假基因、片段重複）是短讀定序的已知盲區，報告需註明；需要時改用長距離 PCR、MLPA 或長讀定序確認。

在 IGV 中，MAPQ 0 的 reads 以透明 / 白色顯示，見 [IGV](../../bioinformatics-tools/visualization/igv.md)。重複序列的來源見 [RepeatMasker](../../bioinformatics-tools/ngs-tools/repeatmasker.md)。
