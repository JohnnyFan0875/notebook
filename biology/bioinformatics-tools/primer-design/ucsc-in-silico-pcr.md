[生資工具](../README.md) › [引子設計](README.md) › UCSC In-Silico PCR

# UCSC In-Silico PCR

用一對引子在 UCSC 的參考基因體（或轉錄體）上模擬 PCR，回傳所有可能的產物位置與序列，用來確認引子**只產生一個預期產物**。

| 項目 | 內容 |
| --- | --- |
| 網站 | [genome.ucsc.edu/cgi-bin/hgPcr](https://genome.ucsc.edu/cgi-bin/hgPcr) |
| 輸入 | 物種與基因體版本（hg38 / hg19）、Target（genome 或 GENCODE / RefSeq 轉錄體）、正反引子、最大產物長度 |
| 輸出 | 每個產物的位置（可直接開成 Genome Browser 軌道）、長度、序列（引子部分大寫） |
| 參數 | `Min Perfect Match`（3′ 端需完全配對的長度，最小 15）、`Min Good Match`（3′ 端每 3 個鹼基至少 2 個配對的長度）、`Max Product Size` |
| 何時用 | Primer3 設計後檢查專一性；確認產物是否跨 exon（Target 選轉錄體） |
| 限制 | 只找高度相似的結合位置，對有少數錯配的非專一結合不敏感；完整檢查用 [Primer-BLAST](https://www.ncbi.nlm.nih.gov/tools/primer-blast/) |

> 選錯基因體版本是最常見的錯誤：hg19 與 hg38 的座標不同；回報位置時要註明版本。產物出現在 Genome Browser 後，順便打開 dbSNP 與 RepeatMasker 軌道，檢查引子下是否有 SNP 或重複序列。

相關：[UCSC Genome Browser](../../genetics/databases/gene/ucsc-genome-browser.md)、[引子設計準則](README.md)。
