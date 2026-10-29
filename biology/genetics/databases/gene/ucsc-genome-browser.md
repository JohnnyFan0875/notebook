[資料庫](../README.md) › [基因](README.md) › UCSC Genome Browser

# UCSC Genome Browser

互動式基因組瀏覽器：在同一個座標區域疊加基因、保守性、重複序列、調控、變異與自訂軌道，是目視檢查區域與下載註解表格的常用工具。

| 存取方式 | 用途 |
| --- | --- |
| [Genome Browser](https://genome.ucsc.edu/) | 瀏覽區域、疊加軌道 |
| [Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables) | 依區域 / 基因下載任一軌道的表格、BED、序列 |
| [Downloads](https://hgdownload.soe.ucsc.edu/downloads.html) | FASTA、註解資料庫表格、liftOver chain |
| [In-Silico PCR](../../../bioinformatics-tools/primer-design/ucsc-in-silico-pcr.md)、BLAT、liftOver | 引子檢查、序列比對、版本轉換 |

| 常用軌道 | 用途 |
| --- | --- |
| GENCODE / NCBI RefSeq / MANE | 基因結構與轉錄本 |
| Conservation（phyloP、phastCons） | 跨物種保守性，支持變異的功能重要性 |
| RepeatMasker、Segmental Dups | 重複區、假基因造成比對困難的區域 |
| dbSNP、gnomAD、ClinVar | 已知變異與臨床分類 |
| ENCODE cCREs | 候選調控元件 |

可上傳 BED、VCF、BAM、bigWig 作為自訂軌道（大檔用 bigBed / bigWig + URL）。

> 網頁顯示是 **1-based**，Table Browser 匯出的 BED 是 **0-based**（見 [座標系統](../../../genomics/file-formats/zero-one-based.md)）。截圖或匯出表格作為證據時，記錄基因組版本與軌道版本。
