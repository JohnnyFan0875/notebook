[基因體學](../README.md) › [定序技術](README.md) › 定序平台

# 定序平台 (Sequencing Platforms)

定序技術決定了 read 長度、錯誤型態與成本，也決定了下游該檢查哪些品質指標、哪些變異容易漏掉。短讀定序（Illumina 等）準確、便宜，適合 SNV / 小 indel 與定量；長讀定序（PacBio、ONT）能跨越重複區，適合結構變異、單倍型與組裝。

## 平台比較

| 平台 | 原理 | read 長度 | 主要錯誤型態 | 強項 |
| --- | --- | --- | --- | --- |
| Illumina（NovaSeq、NextSeq、MiSeq） | 可逆終止子邊合成邊定序 (SBS) | 50–300 bp（成對） | 置換為主，約 0.1–0.5%；尾端品質下降 | 產量大、準確、生態系最完整 |
| MGI DNBSEQ、Element AVITI | DNA nanoball / avidity 定序（短讀 SBS 類） | 100–300 bp | 置換為主 | 成本、品質與 Illumina 相近 |
| Ion Torrent | 半導體偵測 pH 變化 | 200–600 bp | **homopolymer 長度錯誤**（indel） | 快、amplicon panel |
| Ultima（UG 100） | 流動式 (flow-based) 定序 | ~300 bp 單端 | homopolymer indel | 每 Gb 成本低 |
| PacBio HiFi（Revio、Sequel II） | 單分子即時定序；環狀共識 (CCS) | 15–25 kb | 單次讀取錯誤高，CCS 後 > Q30 | 長且準：SV、phasing、組裝、全長轉錄本 |
| Oxford Nanopore（MinION、PromethION） | 分子穿過奈米孔的電流變化 | 數 kb 到 > 1 Mb | homopolymer / 甲基化區的 indel；隨化學與 basecaller 改善（R10.4.1 可達 Q20+） | 超長讀、即時、直接偵測甲基化與 RNA 修飾、可攜 |

## 錯誤型態 → 要檢查什麼

| 平台特性 | 對分析的影響 | 對應 QC / 處理 |
| --- | --- | --- |
| 短讀 | 重複區、假基因、片段重複比對不唯一 | [MAPQ](../ngs-qc/mapping-quality.md)、標記低信心區域 |
| PCR 擴增 | 重複 reads、GC 偏差 | [重複率](../ngs-qc/duplication-rate.md)、[GC 偏差](../ngs-qc/gc-bias.md) |
| 置換錯誤、尾端品質下降 | 偽 SNV | [鹼基品質](../ngs-qc/base-quality-scores.md)、修剪、BQSR |
| homopolymer indel（Ion Torrent、ONT） | 偽 indel，特別是 `AAAAAA` 類序列 | 平台專用的 caller（如 Clair3、DeepVariant 的對應模型）、對 homopolymer 區 indel 提高門檻 |
| 2-channel 無訊號 = G | 假 polyG 尾巴 | 見下方；fastp `--trim_poly_g` |
| 長讀但單次錯誤率高 | 需共識或專用模型 | HiFi CCS、ONT 的 SUP basecalling 與 duplex |

## Illumina 2-channel 化學與 polyG

舊機型（HiSeq 2500、MiSeq）每個 cycle 拍 4 張影像（每種鹼基一個顏色）；NextSeq、NovaSeq、MiSeq i100 改用 **2-channel**：只拍紅、綠兩張，以組合判斷鹼基，速度較快。iSeq 100 則是 1-channel。

| 訊號 | 鹼基（Illumina 紅 / 綠範例） |
| --- | --- |
| 只有紅 | C |
| 只有綠 | T |
| 紅 + 綠 | A |
| **都沒有（暗）** | **G** |

不同 2-channel 系統的顏色指派可能不同，但「暗 = G」是共同特性。因此當片段比 read 短、或 cluster 訊號衰減時，儀器讀到的是「沒有訊號」，被判成一串 **G**（polyG 尾巴）；這不是真實序列，要在比對前修剪（[fastp](../../bioinformatics-tools/ngs-tools/fastp.md) 對 NextSeq / NovaSeq 資料自動開啟）。參考：[Illumina 2-channel SBS](https://emea.illumina.com/science/technology/next-generation-sequencing/sequencing-technology/2-channel-sbs.html)。

## 依應用選擇

| 應用 | 常見選擇 | 說明 |
| --- | --- | --- |
| WGS（germline SNV / indel） | Illumina 30× | 標準、便宜 |
| 結構變異、重複擴增、phasing | PacBio HiFi、ONT | 短讀難以跨越 |
| WES / 標靶 panel | Illumina、Ion Torrent | 見 [標靶定序](targeted-panels.md) |
| bulk RNA-seq 定量 | Illumina 2×100–150 | 見 [RNA-seq](../workflows/rna-seq/README.md) |
| 全長轉錄本、isoform | PacBio Iso-Seq、ONT cDNA / direct RNA | 不需拼接推論 isoform |
| DNA 甲基化 | 亞硫酸鹽 / EM-seq + Illumina；或 PacBio / ONT 直接偵測 | 長讀不需化學轉換 |
| 單細胞 | 10x Genomics + Illumina | 見 [單細胞 RNA-seq](single-cell-rna-seq/README.md) |
| 液態切片 | 深度定序 + UMI | 見 [液態切片](liquid-biopsy.md) |
| 現場 / 即時（病原體） | ONT MinION | 可攜、即時分析 |

## 延伸資源

| 資源 | 內容 |
| --- | --- |
| [Enseqlopedia](https://enseqlopedia.com/enseqlopedia/) | James Hadfield 維護的 NGS 資源站：定序方法 wiki（RNA、DNA、表觀遺傳）、各定序儀分布地圖 (NGS Mapped)、Core Genomics 部落格；部分條目可能過時，以原始文獻為準 |
| 各廠商規格頁 | read 長度、產量、錯誤率依機型與化學版本更新快，引用時以官方最新規格為準 |
