[Biology](../../README.md) › [基因體學](../README.md) › 全基因體分析

# 全基因體分析 (Genome-Wide Analysis)

在整個基因組上系統性地尋找與性狀、疾病或分子表現量相關的遺傳變異，再透過整合不同層次的資料，從「關聯位點」推進到「可能的致病基因與機制」。

## 建議順序

```
GWAS（變異 ↔ 疾病 / 性狀）
  └─► QTL（變異 ↔ 分子表現量）：eQTL（表現量）、sQTL（剪接）、pQTL（蛋白質）
        └─► Colocalization（兩個訊號是否來自同一個致病變異）→ 候選基因
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [GWAS 基礎](gwas-fundamental.md) | QC、族群結構、關聯檢定、Manhattan / QQ、fine-mapping、PRS | 哪些變異與性狀有關？ |
| [QTL 分析](qtl-analysis-and-mapping.md) | 連鎖 vs 關聯定位、cis / trans、統計框架 | 怎麼找影響數量性狀的位點？ |
| [eQTL](eqtl.md) | 表現量 QTL、GTEx、隱藏共變數 | 這個變異改變哪個基因的表現量？ |
| [sQTL](sqtl.md) | 剪接 QTL、LeafCutter | 這個變異改變剪接嗎？ |
| [pQTL](pqtl.md) | 蛋白質 QTL、平台假象 | 這個變異改變蛋白質濃度嗎？ |
| [Colocalization](colocalization.md) | coloc、SuSiE、eCAVIAR | GWAS 與 eQTL 訊號是同一個致病變異嗎？ |

統計基礎：[多重檢定](../../../data-science/statistics/inferential-statistics/multiple-testing.md)、[PCA（族群結構）](../../../data-science/statistics/multivariate-analysis/pca.md)、[混合效應模型（親緣關係）](../../../data-science/statistics/regression-analysis/mixed-effects-models.md)。變異資料庫見 [GWAS Catalog](../../genetics/databases/variant/gwas-catalog.md)、[GTEx](../../genetics/databases/functional-expression/gtex.md)。
