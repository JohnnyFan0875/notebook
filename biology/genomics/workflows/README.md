[Biology](../../README.md) › [基因體學](../README.md) › 分析流程

# 分析流程 (Analysis Workflows)

從原始資料到生物學結論的完整分析流程。工具指令見 [NGS 工具](../../bioinformatics-tools/ngs-tools/README.md)；R 物件見 [Bioconductor](../../bioinformatics-tools/bioconductor.md)；用工作流引擎串接見 [Nextflow](../../../computing/workflow-engines/nextflow/README.md)。

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [RNA-seq 分析](rna-seq/README.md) | 10 章：FASTQ QC → 比對 / 定量 → 標準化 → EDA → edgeR / DESeq2 / limma-voom → 富集 → 可重現性 | 哪些基因在不同條件下表現改變？ |
| [變異呼叫](variant-calling.md) | GATK germline 流程、VQSR vs 硬過濾、Mutect2 somatic、正規化與註解 | 樣本帶有哪些 SNV / indel？哪些是真的？ |
| [limma](limma-differential-expression.md) | 線性模型 + 經驗貝氏、設計矩陣與對比、批次、基因集檢定 | microarray / 連續型資料怎麼做差異分析？複雜設計怎麼寫？ |
| [Precision Medicine Bioinformatics](pmbio.md) | 外部課程：比對、germline / somatic 變異呼叫、RNA-seq、臨床解讀 | 想跟著完整課程從頭做一次 |

