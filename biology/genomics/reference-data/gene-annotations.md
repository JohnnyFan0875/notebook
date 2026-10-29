[基因體學](../README.md) › [參考資料](README.md) › 基因註解

# 基因註解 (Gene Annotations)

基因註解定義基因、轉錄本、exon 與 CDS 的位置。同一個基因在不同註解系統中可能有不同的轉錄本數量與 ID，**選哪一套會直接影響 RNA-seq 計數、變異的效應判定與 HGVS 命名**。格式見 [GTF / GFF3](../file-formats/gtf-gff.md)。

## 主要註解系統

| 系統 | ID 範例 | 特點 | 下載 |
| --- | --- | --- | --- |
| GENCODE | `ENSG…`、`ENST…`（與 Ensembl 相同） | 人 / 小鼠的參考註解，含人工審閱（HAVANA）；`chr` 命名 | [gencodegenes.org](https://www.gencodegenes.org/human/) |
| Ensembl | 同上 | 與 GENCODE 內容相同、命名 `1`；多物種 | [Ensembl FTP current_gtf](https://ftp.ensembl.org/pub/current_gtf/homo_sapiens/) |
| NCBI RefSeq | `NM_`（mRNA）、`NR_`（非編碼）、`NP_`（蛋白）；`XM_` / `XR_` 為預測 | 較保守、轉錄本較少；臨床報告傳統上使用 | [NCBI GRCh38_latest](https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/) |
| RefSeqGene | `NG_` | 以基因為中心的參考區段（含上下游），用於 HGVS 的 `g.` 座標 | [RefSeqGene FTP](https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/) |
| **MANE** | `NM_000546.6` ↔ `ENST00000269305.9`（TP53） | NCBI 與 EMBL-EBI 共同選定、**序列完全一致**的轉錄本對 | [NCBI MANE](https://www.ncbi.nlm.nih.gov/refseq/MANE/) |
| UCSC refGene / ncbiRefSeq | `NM_…` | UCSC 對 RefSeq 的比對結果；`ncbiRefSeqSelect` 只留每個基因一個轉錄本 | [UCSC hg38 database](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/)（`ncbiRefSeqSelect.txt.gz`） |

> 版本號是 ID 的一部分：`NM_000546.6` 與 `NM_000546.5` 序列可能不同，HGVS 命名必須帶版本號。

## MANE：臨床報告的預設轉錄本

| 集合 | 內容 | 用途 |
| --- | --- | --- |
| MANE Select | 幾乎每個蛋白編碼基因一個代表性轉錄本 | 臨床變異命名的預設、資料庫之間對齊 |
| MANE Plus Clinical | 少數基因額外的轉錄本 | 有臨床意義的變異落在 Select 以外的轉錄本時 |

同一個變異在不同轉錄本上的 `c.` 位置、甚至效應（missense vs intronic）都可能不同；使用 MANE Select 讓 ClinVar、gnomAD、VEP 與報告講同一種語言。命名規則見 [HGVS 命名](../../genetics/variant-interpretation/hgvs-nomenclature.md)。

## GENCODE 的版本與子集

| 檔案 | 內容 | 何時用 |
| --- | --- | --- |
| `gencode.vXX.annotation.gtf` | comprehensive：主要染色體的所有轉錄本 | RNA-seq 計數（STAR、featureCounts） |
| `gencode.vXX.basic.annotation.gtf` | 只留 `tag "basic"` 的完整轉錄本 | 想減少片段化 / 不完整轉錄本 |
| `gencode.vXX.chr_patch_hapl_scaff.annotation.gtf` | 含 alt / patch 序列 | 比對到含 alt 的參考時 |
| `gencode.vXX.transcripts.fa` | 轉錄本序列 | Salmon / kallisto 索引 |

## 選擇指引

| 情境 | 建議 |
| --- | --- |
| RNA-seq 定量 | GENCODE comprehensive 或 Ensembl；FASTA、GTF、Salmon 索引同一版本 |
| 臨床變異命名與報告 | MANE Select（必要時 Plus Clinical） |
| 變異效應註解（VEP） | 同時輸出 Ensembl 與 RefSeq，並以 `--mane` / `--pick` 標出 MANE |
| 與舊臨床報告比對 | 確認當時使用的 RefSeq 轉錄本與版本 |
| 跨研究合併 | 統一到同一套註解與版本；ID 去掉版本號再對應 |

相關：[參考基因組](reference-genomes.md)、[Ensembl](../../genetics/databases/gene/ensembl.md)、[NCBI Gene](../../genetics/databases/gene/ncbi-gene.md)、[Ensembl VEP](../../genetics/databases/variant/ensembl-vep.md)。
