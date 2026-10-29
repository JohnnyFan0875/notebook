[基因體學](../README.md) › [癌症基因體](README.md) › TCGA 與 GDC

# TCGA 與 Genomic Data Commons (GDC)

TCGA（The Cancer Genome Atlas）是 NCI 與 NHGRI 主導的計畫，對 33 種癌症、超過 11,000 位病人做了基因組、轉錄體、甲基化、蛋白質與臨床資料的系統性定序。資料現由 NCI 的 GDC 統一管理，並以 GRCh38 重新處理 (harmonized)；GDC 也收錄 TARGET、CPTAC 等其他計畫。

| 項目 | 內容 |
| --- | --- |
| 入口 | [GDC Data Portal](https://portal.gdc.cancer.gov/) |
| 資料類型 | WES / WGS 變異（MAF）、RNA-seq counts（STAR）、miRNA、甲基化陣列、CNV、臨床與存活、病理影像 |
| 存取權限 | **開放**：處理後的摘要（counts、遮蔽過的 MAF、CNV 區段）；**受控**：原始 BAM、germline 變異，需 dbGaP 申請 |
| 下載 | 網頁加入購物車 → manifest → [gdc-client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)；或 GDC API |

## 分析工具

| 工具 | 用途 | 何時用 |
| --- | --- | --- |
| TCGAbiolinks（R） | 查詢、下載、整理成 SummarizedExperiment | 程式化取得資料做分析 |
| [cBioPortal](https://www.cbioportal.org/) | 突變、CNV、表現量的互動瀏覽與存活分析 | 快速查某基因在各癌別的變異頻率 |
| [UCSC Xena](https://xenabrowser.net/) | 多體學資料視覺化與下載（含 TCGA Pan-Cancer） | 跨癌別比較、直接下載整理好的矩陣 |
| GEPIA | 腫瘤 vs 正常表現量、存活 | 簡單的表現量查詢 |

```r
library(TCGAbiolinks)
q <- GDCquery(project = "TCGA-LUAD", data.category = "Transcriptome Profiling",
              data.type = "Gene Expression Quantification", workflow.type = "STAR - Counts")
GDCdownload(q)
se <- GDCprepare(q)        # SummarizedExperiment：counts + 臨床資訊（見 Bioconductor 筆記）
# 依 TCGAbiolinks 官方文件整理，未在本機實跑（需連線下載）
```

## 使用注意

| 注意 | 說明 |
| --- | --- |
| 正常對照 | TCGA 的「正常組織」多為腫瘤旁組織，數量少，且不一定真正正常；要比較正常組織可搭配 GTEx（注意批次差異） |
| 批次與中心 | 樣本來自多個收案中心與定序批次；分析時檢查批次（TCGA barcode 含中心與 plate 資訊） |
| 腫瘤純度 | bulk 樣本混有基質與免疫細胞，表現量與 VAF 都受影響 |
| 族群代表性 | 以歐裔為主 |
| 臨床資料品質 | 存活追蹤時間與治療紀錄不完整，建議使用 TCGA Pan-Cancer Clinical Data Resource（TCGA-CDR）的整理版 |
| barcode | `TCGA-05-4244-01A`：`01`–`09` 為腫瘤、`10`–`19` 為正常；同一病人的多個樣本要能對應 |

相關：[Bioconductor：SummarizedExperiment](../../bioinformatics-tools/bioconductor.md#表現量矩陣summarizedexperiment)、[RNA-seq 分析](../workflows/rna-seq/README.md)、[存活分析](../../../data-science/statistics/survival-analysis/README.md)。
