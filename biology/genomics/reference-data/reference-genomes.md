[基因體學](../README.md) › [參考資料](README.md) › 參考基因組

# 參考基因組 (Reference Genomes)

比對、變異座標、註解都以參考基因組為座標系。人類有兩個主流版本，且同一版本有 UCSC、Ensembl、NCBI 三種「包裝」，染色體命名與內容略有不同，**混用是最常見的錯誤來源之一**。

## 人類基因組版本

| 版本 | UCSC 名稱 | 發布 | 特點 | 使用情境 |
| --- | --- | --- | --- | --- |
| GRCh37 | hg19 | 2009 | 舊版；許多舊資料庫與臨床報告仍使用 | 舊資料、部分臨床實驗室 |
| GRCh38 | hg38 | 2013（持續以 patch 更新，如 p14） | 修正數千個錯誤與 gap；含 alt contig、著絲點模型 | **目前主流** |
| T2T-CHM13 | hs1 | 2022 | 第一個無 gap 的完整人類基因組（含著絲點、rDNA） | 研究難比對區域；臨床與資料庫生態尚在轉移中 |

> 座標在版本間不相容：同一個變異在 hg19 與 hg38 的位置可差數千到數百萬 bp。所有資料（BAM、VCF、BED、資料庫）先確認版本。

## UCSC vs Ensembl vs NCBI

| | UCSC | Ensembl | NCBI (RefSeq) |
| --- | --- | --- | --- |
| 染色體名稱 | `chr1`…`chrX`、`chrY`、`chrM` | `1`…`X`、`Y`、`MT` | `NC_000001.11`… |
| 對應註解 | GENCODE、refGene / ncbiRefSeq | Ensembl GTF | RefSeq GFF / GTF |
| 下載 | [hgdownload](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/) | [Ensembl FTP](https://ftp.ensembl.org/pub/current_fasta/homo_sapiens/dna/) | [NCBI GRCh38_latest](https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/) |

> **hg19 的粒線體陷阱**：UCSC hg19 的 `chrM` 是舊的 NC_001807，GRCh37 的 `MT` 是現行標準 rCRS（NC_012920），兩者長度與序列不同；hg38 已統一為 rCRS。

## 該下載哪個 FASTA

| 檔案 | 內容 | 建議 |
| --- | --- | --- |
| **analysis set**（`GCA_000001405.15_GRCh38_no_alt_analysis_set`） | 主要染色體 + 未定位 contig + decoy / EBV，alt contig 移除，PAR 區遮蔽 | **短讀比對首選**（GATK、多數流程） |
| Ensembl `dna.primary_assembly` | 主要染色體 + 未定位 contig，不含 alt / patch | RNA-seq（搭配 Ensembl GTF） |
| GENCODE `primary_assembly.genome.fa` | 同上，`chr` 命名 | RNA-seq（搭配 GENCODE GTF） |
| Ensembl `dna.toplevel` | 含所有 alt haplotype 與 patch | **不要直接拿來比對**：alt contig 會讓真實 reads 變成多重比對、MAPQ 0 |
| `dna_sm` / `dna_rm` | 軟遮蔽（重複區小寫）/ 硬遮蔽（重複區 N） | 引子設計用軟遮蔽；比對用未遮蔽或軟遮蔽，不要用硬遮蔽 |
| UCSC `chromosomes/` | 每條染色體一個檔案 | 只需要少數染色體時 |

alt contig 要保留時，比對器需支援 alt-aware 模式（BWA 的 `.alt` 檔、DRAGEN）。

## 取出特定區域 / 所有 exon 的序列

```bash
samtools faidx GRCh38.fa chr7:140753300-140753400                 # 單一區域
bedtools getfasta -fi GRCh38.fa -bed exons.bed -name -s > exons.fa  # 依 BED（-s 依股別反向互補）
gffread -w transcripts.fa -g GRCh38.fa gencode.gtf                  # 所有轉錄本的序列
```

所有 exon 的 BED 可從 GTF 轉出（見 [GTF / GFF3](../file-formats/gtf-gff.md)），或用 [UCSC Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables)（track 選 GENCODE / NCBI RefSeq，output format 選 *sequence*，再選 *Exons*）。做法參考 [Biostars 討論](https://www.biostars.org/p/67847/#67892)。

## 版本轉換 (liftOver)

| 工具 | 輸入 | 備註 |
| --- | --- | --- |
| [UCSC liftOver](https://genome.ucsc.edu/cgi-bin/hgLiftOver) | BED、座標 | 網頁或命令列，需要 chain 檔（如 `hg19ToHg38.over.chain.gz`） |
| CrossMap | BED、VCF、BAM、GFF、bigWig | 支援的格式最多 |
| Picard `LiftoverVcf` | VCF | 同時處理 REF 等位基因在新版本中改變的情況 |
| NCBI Remap | 多種 | 網頁 |

> liftOver 不是無損的：部分區域在新版本中被刪除、拆開或反向，會轉換失敗或落到錯誤位置。**能重新比對就重新比對**；必須轉換時要回報失敗的比例。

相關：[FASTA 格式](../file-formats/fasta.md)、[基因註解](gene-annotations.md)、[比對品質與 alt contig](../ngs-qc/mapping-quality.md)。
