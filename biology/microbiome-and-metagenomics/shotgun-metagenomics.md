[Biology](../README.md) › [微生物體](README.md) › Shotgun 宏基因體

# Shotgun 宏基因體定序 (Shotgun Metagenomics)

把檢體中所有 DNA 打斷後定序，不靠單一標記基因。相較 [16S](16s-analysis.md)，能同時得到種 / 菌株層級的組成、功能基因與通路、抗藥基因，還能組裝出新的微生物基因體；代價是成本、運算量與對宿主 DNA 的敏感度都較高。

## 流程

```text
raw FASTQ → QC / 修剪（fastp）→ 去除宿主 reads（比對人類參考）
   ├─► 讀段層級 (read-based)：分類定量（MetaPhlAn / Kraken2 + Bracken）
   │                         功能定量（HUMAnN：基因家族 → 通路）
   └─► 組裝層級 (assembly-based)：組裝（MEGAHIT / metaSPAdes）→ binning（MetaBAT2 / SemiBin2）
                                  → MAG 品質（CheckM2）→ 分類（GTDB-Tk）→ 註解
```

| 步驟 | 常用工具 | 輸出 / 檢查點 |
| --- | --- | --- |
| QC | [fastp](../bioinformatics-tools/ngs-tools/fastp.md) | 去 adapter、低品質；保留率 |
| 去宿主 | Bowtie2 對 GRCh38（或 T2T-CHM13）、KneadData、Hostile | 宿主 reads 比例（糞便通常 < 5%，組織 / 拭子可 > 90%）；上傳公開資料庫前也必須去除以保護隱私 |
| 分類定量 | MetaPhlAn 4（物種專一標記基因）、Kraken2 + Bracken（k-mer）、sylph | 物種相對豐度；Kraken2 依資料庫可能有大量偽陽性，需設信心閾值 |
| 功能定量 | HUMAnN 3/4 | 基因家族（UniRef90）、MetaCyc 通路豐度 |
| 抗藥基因 | RGI（CARD）、AMRFinderPlus | 抗藥基因與突變 |
| 菌株 | StrainPhlAn、inStrain | 菌株追蹤（如 FMT 後的定殖） |
| 組裝與 binning | MEGAHIT、metaSPAdes → MetaBAT2、SemiBin2 | contig、MAG |
| MAG 品質 | CheckM2、GUNC | MIMAG 高品質：完整度 > 90%、汙染 < 5%（另需 rRNA 與 tRNA） |
| MAG 分類 | GTDB-Tk | 對應 [GTDB](microbiome-databases.md) 分類 |

## 讀段 vs 組裝

| | Read-based | Assembly-based |
| --- | --- | --- |
| 依賴 | 參考資料庫 | 定序深度與群落複雜度 |
| 優點 | 快、低豐度菌也能定量 | 可發現新物種 / 新基因、基因的基因體脈絡 |
| 缺點 | 資料庫沒有的菌看不到 | 低豐度菌組不起來、運算量大 |

## 設計考量

| 議題 | 建議 |
| --- | --- |
| 深度 | 分類定量約 5–10M reads / 樣本；組裝與菌株分析需 20M 以上 |
| 低菌量檢體 | 宿主 DNA 多、汙染比例高：加做萃取空白、考慮宿主 DNA 去除試劑 |
| 長讀定序 | PacBio HiFi / ONT 可組出完整環狀基因體與質體，見[定序平台](../genomics/sequencing-techniques/sequencing-platforms.md) |
| 統計 | 仍是組成資料，差異豐度的做法與 [16S](16s-analysis.md#組成資料與差異豐度) 相同 |
| 衍生方法 | Metatranscriptomics（RNA，量測「正在表現」的功能）、病毒體 (virome)、臨床 mNGS（未知病原診斷） |

> QIIME 2 的 MOSHPIT 套件把組裝、binning、註解包成同一框架；公開的分析流程（nf-core/mag、nf-core/taxprofiler）可直接用 [Nextflow](../../computing/workflow-engines/nextflow/README.md) 執行。
