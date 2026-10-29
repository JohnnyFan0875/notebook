[基因體學](../README.md) › [分析流程](README.md) › pmbio

# Precision Medicine Bioinformatics (pmbio)

Griffith Lab（McDonnell Genome Institute, WashU）製作的免費線上課程，以癌症精準醫療為主軸，從雲端環境設定一路做到變異判讀與個人化癌症疫苗設計。

| 項目 | 內容 |
| --- | --- |
| 網站 | [pmbio.org/course](https://pmbio.org/course/)（教材以 CC BY-SA 4.0 授權，原始碼在 GitHub） |
| 適合 | 有基本 Linux 經驗、想實際跑過完整 DNA / RNA 定序分析的人 |
| 進行方式 | 模組依序進行，後面的模組沿用前面產生的資料；在 AWS 雲端環境操作 |

| 模組 | 內容 | 本筆記本對應 |
| --- | --- | --- |
| Setup | AWS、UNIX、軟體安裝 | [computing](../../../computing/README.md) |
| Inputs | 參考基因組、註解、索引、原始資料、比對前 QC | [參考資料](../reference-data/README.md)、[FastQC](../../bioinformatics-tools/ngs-tools/fastqc.md) |
| Alignment | 比對、IGV、比對後 QC | [samtools](../../bioinformatics-tools/ngs-tools/samtools.md)、[IGV](../../bioinformatics-tools/visualization/igv.md) |
| Germline | SNV / indel 呼叫、過濾、註解、複核 | [VQSR vs 硬過濾](../ngs-qc/vqsr.md)、[VCF](../file-formats/vcf.md) |
| Somatic | SNV / indel、SV、CNV、LOH | [癌症基因體](../cancer-genomics/README.md) |
| RNAseq | 表現量估計、差異表現、kallisto、融合基因 | [RNA-seq 分析](rna-seq/README.md) |
| Clinical | germline 與 somatic 變異的臨床解讀 | [變異判讀](../../genetics/variant-interpretation/README.md) |
| Immune | 免疫基因體、新抗原與個人化癌症疫苗 | [免疫學](../../immunology/README.md) |
| CWL | Common Workflow Language | [工作流引擎](../../../computing/workflow-engines/README.md) |
| Appendix | ChIP-seq、ggplot2、資料清理 | [ChIP-seq](../sequencing-techniques/chip-seq.md) |
