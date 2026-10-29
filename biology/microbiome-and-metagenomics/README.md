[Biology](../README.md) › 微生物體

# 微生物體與宏基因體 (Microbiome & Metagenomics)

用定序描述微生物群落「有誰、有多少、能做什麼」，以及腸道菌相相關的臨床應用。分析上最大的特點是資料為**組成資料**（相對豐度）、稀疏且高度依賴參考資料庫，統計方法要跟著調整。

建議順序：16S vs shotgun（下表）→ [16S 分析](16s-analysis.md) → [Shotgun 宏基因體](shotgun-metagenomics.md) → [資料庫](microbiome-databases.md) → 臨床應用

## 16S vs Shotgun

| | 16S rRNA 擴增子定序 | Shotgun 宏基因體定序 |
| --- | --- | --- |
| 定序對象 | 16S 基因的高變異區（細菌 / 古菌） | 檢體中所有 DNA（含真菌、病毒、宿主） |
| 分類解析度 | 通常到屬 (genus) | 種 (species)，部分可到菌株 (strain) |
| 功能資訊 | 只能預測（PICRUSt2） | 直接量測基因與通路（HUMAnN） |
| 成本 / 深度 | 低；每樣本數萬 reads 即可 | 高；分類約 5–10M reads，組裝需更多 |
| 宿主 DNA | 不受影響（只擴增 16S） | 低菌量檢體（組織、血液）宿主 reads 可 > 90% |
| 偏差來源 | 引子偏好、16S 拷貝數差異 | 萃取效率、資料庫完整度 |
| 適合 | 大樣本數的群落結構比較 | 物種 / 功能 / 抗藥基因、組裝新基因體 (MAG) |

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [16S 分析](16s-analysis.md) | 高變異區、DADA2 / QIIME 2 流程、ASV vs OTU、α / β 多樣性、組成資料與差異豐度 | 怎麼從擴增子 reads 得到菌相與統計結果？ |
| [Shotgun 宏基因體](shotgun-metagenomics.md) | 去宿主、分類與功能定量、組裝與 MAG binning | 何時需要 shotgun？流程與工具怎麼選？ |
| [微生物體資料庫](microbiome-databases.md) | SILVA、Greengenes2、GTDB、RDP、UNITE、功能資料庫、公開資料集 | 分類指派用哪個資料庫？版本怎麼記錄？ |
| [益生菌 / 益生元 / 後生元](biotics.md) | ISAPP 定義、機制、證據強度 | 這些名詞的正式定義是什麼？哪些效果有證據？ |
| [糞便微生物植入 (FMT)](fmt-fecal-microbiota-transplant.md) | 適應症、核准產品、捐贈者篩檢、風險 | FMT 用在哪裡？安全性怎麼控管？ |
| [腸道通透性](intestinal-permeability.md) | 腸道屏障、乳果糖 / 甘露醇試驗、生物標記、「腸漏症」的證據 | 怎麼量測腸道通透性？L/M 比值怎麼判讀？ |

相關：[定序平台](../genomics/sequencing-techniques/sequencing-platforms.md)、[原始資料庫 SRA / ENA](../genomics/reference-data/raw-data-repositories.md)、[雙變數相關（組成資料的假相關）](../../data-science/statistics/descriptive-statistics/bivariate.md)、[PCA](../../data-science/machine-learning/unsupervised-learning/dimensionality-reduction/pca.md)、[多重檢定](../../data-science/statistics/inferential-statistics/multiple-testing.md)。
