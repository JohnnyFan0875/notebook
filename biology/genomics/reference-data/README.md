[Biology](../../README.md) › [基因體學](../README.md) › 參考資料

# 參考資料 (Reference Data)

分析之前要先準備好三樣東西：參考基因組 (FASTA)、基因註解 (GTF / GFF)，以及要重新分析的公開原始資料。三者的版本與染色體命名必須一致。

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [參考基因組](reference-genomes.md) | GRCh37 / GRCh38 / T2T、UCSC vs Ensembl vs NCBI、該下載哪個 FASTA、liftOver | 該用哪個版本、哪個檔案？座標怎麼轉換？ |
| [基因註解](gene-annotations.md) | GENCODE / Ensembl、RefSeq、MANE Select、UCSC refGene | 用哪套轉錄本？臨床報告該用哪個 transcript？ |
| [原始資料庫](raw-data-repositories.md) | SRA、ENA、DDBJ、GEO、dbGaP / EGA、下載方式 | 公開的 FASTQ / 表現量資料去哪裡找、怎麼下載？ |

## 一套「互相相容」的組合

| 用途 | UCSC / GENCODE 風格（`chr1`） | Ensembl 風格（`1`） |
| --- | --- | --- |
| FASTA | `GRCh38_no_alt_analysis_set` 或 GENCODE `GRCh38.primary_assembly.genome.fa` | `Homo_sapiens.GRCh38.dna.primary_assembly.fa` |
| GTF | GENCODE `gencode.vXX.annotation.gtf` | `Homo_sapiens.GRCh38.XXX.gtf` |
| 已知變異 | GATK resource bundle（dbSNP、gnomAD） | Ensembl variation |
| 適用 | GATK、多數臨床流程、UCSC 瀏覽器 | Ensembl VEP、部分 Bioconductor 套件 |

> 記錄每個專案用的**版本號**（GENCODE vXX / Ensembl release XXX / 下載日期），寫在 README 或流程設定檔中；換版本後基因數、轉錄本 ID 都會變，結果不能直接比較。

格式說明見 [FASTA](../file-formats/fasta.md)、[GTF / GFF3](../file-formats/gtf-gff.md)；變異標準集 (GIAB) 見 [Genome in a Bottle](../assay-validation/reference-standard.md#genome-in-a-bottle-giab)。
