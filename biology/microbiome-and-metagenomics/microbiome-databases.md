[Biology](../README.md) › [微生物體](README.md) › 資料庫

# 微生物體資料庫 (Microbiome Databases)

微生物體分析的結果高度依賴參考資料庫：同一批 reads 用不同資料庫或版本，分類名稱與解析度都會不同。報告時必須寫明資料庫名稱、版本與分類器。

## 分類學參考（16S / 標記基因）

| 資料庫 | 內容 | 現況（2026 查核） | 何時用 |
| --- | --- | --- | --- |
| [SILVA](https://www.arb-silva.de/) | 細菌、古菌、真核的 SSU / LSU rRNA，人工審閱的比對與分類 | SSU 144（2026-08）、LSU 138.2 | 16S / 18S 分類指派的預設選擇；DADA2、QIIME 2 都有現成格式 |
| Greengenes2（McDonald et al. 2023） | 以全基因體演化樹為骨架，16S 與 shotgun 共用同一分類 | 2022 年起發布 | 想讓 16S 與 shotgun 結果用一致分類比較 |
| Greengenes（舊版） | 16S 參考 | 13_8 版（2013）後停止更新 | 只為重現舊研究；新分析不建議 |
| RDP | 16S 序列與 RDP Classifier（8-mer naive Bayes） | 網站已下線；Classifier 仍在 SourceForge / GitHub，2024 年更新分類 | 使用 RDP Classifier 時 |
| [GTDB](https://gtdb.ecogenomic.org/) | 以基因體演化重新整理的細菌 / 古菌分類 | R232（2026-04）：約 90 萬基因體、20 萬物種 | MAG 分類（GTDB-Tk）；分類名稱與 NCBI 可能不同 |
| [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) | 所有 GenBank 序列的分類樹 | 持續更新 | Kraken2、BLAST 結果的分類；與其他資料庫對照 |
| [UNITE](https://unite.ut.ee/) | 真菌 ITS 序列 | 持續更新 | 真菌群落（ITS 擴增子） |

> GTDB 與 NCBI 的命名常不一致（如 GTDB 把部分 *Clostridium* 拆成多個屬，名稱帶 `_A`、`_B` 後綴），跨研究比較前先統一分類系統。

## Shotgun 分析用資料庫

| 資料庫 | 用於 | 內容 |
| --- | --- | --- |
| MetaPhlAn 標記基因庫（mpa 資料庫，源自 ChocoPhlAn） | MetaPhlAn、StrainPhlAn | 各物種專一的標記基因 |
| Kraken2 / Bracken 索引 | Kraken2 | 依 RefSeq 或 GTDB 建立的 k-mer 索引；有 Standard、PlusPF 等預建版本 |
| UniRef90 / ChocoPhlAn | HUMAnN | 基因家族註解 |
| MetaCyc、KEGG | HUMAnN、通路分析 | 代謝通路 |
| CARD | RGI | 抗生素抗藥基因與突變 |
| CAZy | dbCAN | 碳水化合物活性酵素（膳食纖維代謝） |

## 公開資料集與入口

| 資源 | 內容 |
| --- | --- |
| [MGnify](https://www.ebi.ac.uk/metagenomics/)（EMBL-EBI） | 公開擴增子 / 宏基因體資料的統一分析結果、MAG 目錄 |
| Human Microbiome Project (HMP) | NIH 人體微生物體計畫的參考資料 |
| curatedMetagenomicData（Bioconductor） | 數十個人類 shotgun 研究的統一處理結果，可直接載入 R |
| GMrepo | 依疾病整理的人類腸道微生物體資料 |
| [SRA / ENA](../genomics/reference-data/raw-data-repositories.md) | 原始 reads；投稿時需上傳並去除宿主 reads |

> 分類器（naive Bayes classifier）要用與擴增區相同的引子區段訓練，並與資料庫版本一起記錄；換版本後同一 ASV 的分類可能改變。
