[基因體學](../README.md) › [檢測確效](README.md) › 參考標準品

# 參考標準品 (Reference Standards)

已知「答案」的樣本或資料，用來評估檢測與生資流程的準確度、偵測極限與跨批穩定性。分成兩類：有實體的標準品（跑濕實驗）與高信心的基準變異集（比對流程輸出）。

## 種類

| 類型 | 例 | 用途 |
| --- | --- | --- |
| 細胞株 DNA | GIAB 細胞株（Coriell NA12878 等） | germline 全流程（萃取 → 定序 → 呼叫） |
| 商業多重突變標準品 | Horizon / Seracare / 其他廠商：已知 VAF 的 SNV、indel、CNV、融合 | 體細胞 panel 的敏感度與 LOD |
| 稀釋系列 | 標準品與野生型 DNA 依比例混合（如 VAF 5%、2.5%、1%、0.5%） | 偵測極限 |
| 模擬 cfDNA / FFPE 基質 | 片段化或福馬林處理的標準品 | 模擬真實樣本型態 |
| 數位基準 (benchmark) | GIAB 高信心變異集、合成資料 | 只評估生資流程 |

> 標準品的基質（DNA 片段大小、FFPE 損傷、cfDNA 型態）要盡量接近臨床樣本 (commutability)；用乾淨的細胞株 DNA 估出的 LOD 會比實際樣本樂觀。

## Genome in a Bottle (GIAB)

NIST 主導的聯盟，對少數公開樣本整合多種定序技術，建立**高信心變異集與高信心區域**，是 germline 流程評估的事實標準。

| 樣本 | 來源 | 說明 |
| --- | --- | --- |
| HG001 | NA12878（歐裔女性） | 最早、最常用 |
| HG002 / HG003 / HG004 | 阿什肯納茲猶太人三人家庭（子 / 父 / 母） | 家庭可驗證遺傳一致性；HG002 是目前資料最完整的樣本 |
| HG005 / HG006 / HG007 | 漢人三人家庭 | 東亞族群 |

| 檔案 | 內容 |
| --- | --- |
| 基準 VCF | 高信心的 SNV / indel（另有 SV、CNV 的基準） |
| 高信心區域 BED | 只在這些區域內計算 TP / FP / FN；區域外的差異不計 |
| 分層 (stratification) BED | 依難度分區：homopolymer、低複雜度、片段重複、高 GC… |
| 特殊基準 | 困難的醫學相關基因 (CMRG)、以 T2T 為基礎的新版基準 |

下載：[GIAB FTP release](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/)（各樣本有 GRCh37 / GRCh38 版本，選與流程相同的基因組版本）。

## 用 GIAB 評估流程

```bash
# hap.py（GA4GH 標準）：會先正規化變異表示法，再比對
hap.py HG002_GRCh38_benchmark.vcf.gz my_calls.vcf.gz \
  -f HG002_GRCh38_benchmark.bed \
  -r GRCh38.fa \
  --stratification GRCh38-stratifications.tsv \
  -o happy_out/HG002
# 輸出 summary.csv：SNP / INDEL 各自的 recall、precision、F1
```

| 原則 | 說明 |
| --- | --- |
| 分開看 SNV 與 indel | indel 通常較差 |
| 看分層結果 | 整體 99.9% 可能掩蓋 homopolymer 區只有 90% |
| 只在目標區域評估 | panel / WES 要把 GIAB 高信心區域與自己的目標 BED 取交集 |
| 用比對工具，不要自己 `diff` | 同一個變異有不同寫法（見 [VCF：同一個變異的不同寫法](../file-formats/vcf.md#同一個變異的不同寫法)）；hap.py / RTG vcfeval 會處理 |
| 流程改版就重跑 | 保留每版的結果做回歸測試 |

指標定義見 [檢測確效](README.md)；變異呼叫流程見 [VQSR vs 硬過濾](../workflows/variant-calling.md#變異過濾vqsr-vs-硬過濾)。中文說明參考：[參考標準品（yourgene）](https://yourgene.pixnet.net/blog/posts/7118001727)。
