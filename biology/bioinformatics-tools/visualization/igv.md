[生資工具](../README.md) › [視覺化](README.md) › IGV

# IGV (Integrative Genomics Viewer)

Broad Institute 開發的基因體瀏覽器，把比對 reads、變異、註解與覆蓋度疊在同一個位置上，是**人工複核 (manual review) 候選變異**的標準工具。

| 版本 | 特點 |
| --- | --- |
| [IGV Desktop](https://igv.org/doc/desktop/) | 本機 Java 程式；可開大型 BAM、批次截圖 |
| [igv.js / IGV-Web](https://igv.org/app/) | 瀏覽器版，可嵌入網頁或 Jupyter（`igv-notebook`） |
| igv-reports | 把一批變異的 IGV 畫面打包成單一 HTML，方便分享與審查 |

## 可載入的檔案

| 類型 | 格式 | 需要的索引 |
| --- | --- | --- |
| 比對 | BAM、CRAM | `.bai`、`.crai`（CRAM 另需參考 FASTA） |
| 變異 | VCF（`.vcf.gz`） | `.tbi`（見 [tabix](../ngs-tools/tabix.md)） |
| 區間 / 註解 | BED、GTF / GFF | 大檔建議 bgzip + tabix |
| 訊號 | bigWig、bedGraph、TDF | — |

> 參考基因體版本必須和檔案一致（hg19 vs hg38），否則 reads 會對到錯的位置或完全不顯示。

## 複核變異時看什麼

| 檢查 | 真變異 | 可疑 |
| --- | --- | --- |
| 支持 reads 數與 VAF | 足夠深度、VAF 合理（germline 約 50% / 100%） | 只有 1–2 條 reads |
| 鏈偏差 (strand bias) | 正反股都有 | 只出現在單一方向（顏色依股別上色） |
| 位置偏差 | 分布在 read 各處 | 都在 read 末端 |
| 比對品質 | MAPQ 高（實心） | MAPQ 0（透明 / 白色）：重複區或假基因 |
| 鹼基品質 | 錯配鹼基顏色深 | 錯配鹼基顏色淡（低品質） |
| 周邊 | 單一變異 | 附近一堆錯配：比對錯誤、未正規化的 indel |
| 重複標記 | 不同片段 | 全部是重複 reads（同起點同終點） |
| 剪接 (RNA-seq) | — | 跨越 exon 邊界的細線（`N` CIGAR）不要誤判成缺失 |

常用操作：依鹼基 / 股別 / 樣本分組 reads（右鍵 *Group by*）、*Sort by base* 把帶變異的 reads 排到上方、*Collapsed* 模式看大範圍覆蓋度。系統化的複核準則可參考 Barnell et al. 2019 的 SOP（Genetics in Medicine）。

相關：[BAM 格式](../../genomics/file-formats/bam.md)、[Mapping Quality](../../genomics/ngs-qc/mapping-quality.md)。
