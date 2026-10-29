[Biology](../README.md) › 生資工具

# 生資工具 (Bioinformatics Tools)

生物資訊分析常用的命令列工具、R 套件與視覺化工具。檔案格式本身見 [檔案格式](../genomics/file-formats/README.md)；分析流程見 [定序分析流程](../genomics/workflows/README.md)；安裝環境（conda / Docker）見 [容器與環境](../../computing/containers-and-env/README.md)。

## 模組

| 模組 | 內容 | 回答的問題 |
| --- | --- | --- |
| [NGS 工具](ngs-tools/README.md) | FastQC、fastp、samtools、Picard、sambamba、bcftools、bedtools、tabix、RepeatMasker | FASTQ / BAM / VCF / BED 要用哪個指令處理？ |
| [Bioconductor](bioconductor.md) | Biostrings、IRanges / GRanges、ShortRead、SummarizedExperiment | 在 R 裡怎麼表示序列、基因體區間與表現量矩陣？ |
| [引子設計](primer-design/README.md) | 設計準則、Primer3、Primer-BLAST、In-Silico PCR、PrimerPooler | 怎麼設計專一、不互相干擾的 PCR 引子？ |
| [視覺化](visualization/README.md) | IGV、BioRender | 怎麼目視檢查 reads / 變異？怎麼畫示意圖？ |

## 一個樣本從 FASTQ 到 VCF 用到的工具

```
FASTQ ──FastQC / fastp──► 乾淨 FASTQ ──比對（BWA / STAR）──► BAM
  ──samtools sort / index──► Picard / sambamba 標記重複 ──► 變異呼叫 ──► VCF
  ──bcftools filter / norm / annotate──► bgzip + tabix ──► 下游判讀
                     IGV 隨時目視檢查 BAM / VCF；bedtools 處理目標區域 BED
```

完整流程與參數選擇見 [RNA-seq 分析](../genomics/workflows/rna-seq/README.md)。
