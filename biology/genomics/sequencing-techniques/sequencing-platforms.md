[基因體學](../README.md) › [定序技術](README.md) › 定序平台

# 定序平台 (Sequencing Platforms)

定序技術決定了 read 長度、錯誤型態與成本，也決定了下游該檢查哪些品質指標、哪些變異容易漏掉。短讀定序（Illumina 等）準確、便宜，適合 SNV / 小 indel 與定量；長讀定序（PacBio、ONT）能跨越重複區，適合結構變異、單倍型與組裝。

## 平台比較

| 平台 | 原理 | read 長度 | 主要錯誤型態 | 強項 |
| --- | --- | --- | --- | --- |
| Illumina（NovaSeq、NextSeq、MiSeq） | 可逆終止子邊合成邊定序 (SBS) | 50–300 bp（成對） | 置換為主，約 0.1–0.5%；尾端品質下降 | 產量大、準確、生態系最完整 |
| MGI DNBSEQ | DNA nanoball（RCA）+ cPAS（短讀 SBS 類） | 100–300 bp | 置換為主 | 每 Gb 成本低；duplicate、index hopping 較少 |
| Element AVITI | 表面原位 RCA + avidity 定序 | 100–300 bp | 置換為主 | 宣稱 Q40 以上、試劑用量低 |
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

## 短讀平台的擴增與定序化學：Illumina、MGI、Element

三家都是「邊合成邊讀取」的短讀定序，差在**怎麼放大訊號**與**怎麼辨識鹼基**。MGI 與 Element 都用滾環複製 (rolling circle amplification, RCA)，但真正拉開差異的是定序化學（cPAS vs avidity），不是 RCA 本身。

| | Illumina | MGI DNBSEQ | Element AVITI |
| --- | --- | --- | --- |
| 訊號放大 | 橋式擴增 (bridge PCR / ExAmp) 在 flow cell 上長出 cluster | 文庫環化後在**溶液中** RCA，製成 DNA nanoball (DNB) | 文庫環化後在 **flow cell 表面原位** RCA，長出 polony |
| 載入 | 原位生成（新機型為 patterned flow cell） | DNB 吸附到規則排列的 patterned array | 表面隨機分布 |
| 定序化學 | SBS：螢光可逆終止子 | cPAS（另有 CoolMPS） | Avidity sequencing |
| 辨識與延伸 | 同一步 | 同一步（CoolMPS 例外，見下） | **分成兩步** |
| 接到鏈上的核苷酸 | 帶螢光，成像後切除 | 帶螢光，成像後切除 | **不帶螢光**的可逆終止子 |
| 設計重點 | 產量、生態系 | 高密度、低成本 | 高準確度、低試劑消耗 |

> RCA 的每個拷貝都從**原始環狀模板**複製（線性放大），錯誤不會像 PCR 一樣一輪輪累積；也沒有 PCR 的 duplicate 與 index hopping 問題。

### cPAS（combinatorial probe-anchor synthesis）

由 Complete Genomics（後被 BGI 收購）發展，源自早期的 cPAL（probe-anchor **ligation**），後來把連接酶改成聚合酶，名稱也從 ligation 變成 synthesis。

```
anchor primer 與 DNB 接頭雜交
  → 聚合酶接上一個帶螢光、可逆終止的核苷酸
  → 成像判讀鹼基
  → 切除螢光與終止子 → 下一循環
```

邏輯與 Illumina SBS 相同，差在跑在 DNB + patterned array 上。**CoolMPS** 是 MGI 的另一種化學：先用未標記的可逆終止子延伸，再用帶螢光的**抗體**辨識剛接上的鹼基；「辨識與延伸分開」的概念接近 avidity，但辨識靠抗體而非多價結合。

### Avidity sequencing

把「讀鹼基」和「延伸鏈」拆開，利用**多價結合 (avidity)** 提高辨識特異性。

| 步驟 | 做什麼 |
| --- | --- |
| 1. 辨識 (binding) | *avidite*：一個核心帶多條「手臂」，每條末端是同一種帶螢光的核苷酸。多條手臂同時結合同一個 polony 上的多個聚合酶–模板複合物，結合力強，所以只需極低濃度；配對正確者停留較久，錯配者很快脫落。**此時核苷酸沒有接上鏈** |
| 2. 成像 | 判讀螢光顏色 |
| 3. 移除 | 洗掉 avidite |
| 4. 延伸 (incorporation) | 加入**不帶螢光**的可逆終止子核苷酸，延伸一個鹼基，再解除終止 |

| 特色 | 原因 |
| --- | --- |
| 準確度高（宣稱 Q40 以上） | 辨識靠多價結合且與延伸分離 |
| 長讀長下品質較穩 | 接上鏈的是無螢光核苷酸，不留染料殘基 (dye scar) |
| 試劑消耗低 | avidite 濃度極低 |

> 廠商的錯誤率數字依機型與化學版本更新快；做技術或成本比較時，對照官方白皮書與原始文獻（Element 的 avidity 論文：Arslan et al., *Nature Biotechnology* 2024）。比較兩平台實際錯誤率的方法見 [SAM / BAM：MD 與 NM](../file-formats/bam.md#md-與-nm錯配與編輯距離)。

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
