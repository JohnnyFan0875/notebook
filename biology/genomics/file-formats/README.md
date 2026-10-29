[Biology](../../README.md) › [基因體學](../README.md) › 檔案格式

# 基因體檔案格式 (Genomics File Formats)

定序分析的每一步都有對應的標準格式。先搞懂座標系統（0-based vs 1-based），再看各格式。

## 資料流與格式

```
FASTA（參考序列）+ GTF/GFF（基因註解）
        │
FASTQ（reads + 品質）──比對──► SAM / BAM / CRAM（比對結果）──變異呼叫──► VCF（變異）
                                  │
                                  └──計數 / 覆蓋度──► count matrix、bigWig、BED（區間）
```

## 筆記

| 格式 | 內容 | 座標 | 常用工具 |
| --- | --- | --- | --- |
| [座標系統](zero-one-based.md) | 0-based 半開 vs 1-based 閉區間、轉換規則 | — | — |
| [FASTA](fasta.md) | 參考序列、`.fai` 索引、軟遮蔽 | — | samtools faidx、seqkit |
| [FASTQ](fastq.md) | reads、品質字串、成對檔案 | — | FastQC、fastp |
| [SAM / BAM / CRAM](bam.md) | 比對結果、FLAG、CIGAR、header | 1-based | samtools、Picard |
| [VCF](vcf.md) | 變異、INFO / FORMAT、基因型 | 1-based | bcftools、GATK |
| [BED](bed.md) | 基因體區間 | **0-based** | bedtools |
| [GTF / GFF3](gtf-gff.md) | 基因、轉錄本、exon 註解 | 1-based | gffread、AGAT |

## 壓縮與索引速查

| 檔案 | 壓縮 | 索引 | 建索引指令 |
| --- | --- | --- | --- |
| FASTA | 不壓縮或 bgzip | `.fai`（+ `.gzi`） | `samtools faidx ref.fa` |
| BAM | 內建 BGZF | `.bai` / `.csi` | `samtools index` |
| CRAM | 依參考序列壓縮 | `.crai` | `samtools index` |
| VCF | bgzip（`.vcf.gz`） | `.tbi` / `.csi` | `tabix -p vcf`、`bcftools index` |
| BED / GFF | bgzip | `.tbi` | `tabix -p bed / gff` |

> **bgzip ≠ gzip**：bgzip 是分塊壓縮，可以隨機存取；一般 `gzip` 壓的檔案無法建索引。

壓縮、索引、查詢的工具見 [NGS 工具](../../bioinformatics-tools/ngs-tools/README.md)；參考序列與註解從哪裡下載見 [參考資料](../reference-data/README.md)。
