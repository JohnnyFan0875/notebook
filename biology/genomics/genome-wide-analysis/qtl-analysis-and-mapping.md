[基因體學](../README.md) › [全基因體分析](README.md) › QTL 分析

# QTL 分析與定位 (QTL Analysis & Mapping)

數量性狀位點 (quantitative trait locus, QTL) 是影響連續性狀的基因組區域。性狀可以是身高、產量這類生物體表型，也可以是分子表型：基因表現量 (eQTL)、剪接 (sQTL)、蛋白質濃度 (pQTL)、代謝物 (mQTL)、甲基化 (meQTL)。

## 兩種定位策略

| | 連鎖定位 (linkage mapping) | 關聯定位 (association mapping) |
| --- | --- | --- |
| 族群 | 家系或實驗雜交（F2、RIL、回交） | 無血緣關係的自然族群 |
| 原理 | 追蹤標記與性狀在世代間的共同傳遞 | 利用歷史重組留下的 LD |
| 解析度 | 低（數 Mb） | 高（數十 kb） |
| 常見於 | 動植物育種、罕見孟德爾疾病 | 人類 GWAS、分子 QTL |

## 分子 QTL 流程

```
基因型 + 分子表型（如 RNA-seq 表現量）
  ──► 表型標準化（log / inverse normal transform）
  ──► 共變數：基因型 PCs + 隱藏因子（PEER、表現量 PCs）+ 已知批次
  ──► 每個基因 × 鄰近變異（cis 窗口，常為 TSS ± 1 Mb）做關聯檢定
  ──► 基因內 permutation → 基因層級 p 值 → 跨基因 FDR
  ──► eGene / lead variant ──► fine-mapping、colocalization
```

| 名詞 | 意義 |
| --- | --- |
| cis-QTL | 變異位在受影響基因附近（同一條染色體，通常 ±1 Mb） |
| trans-QTL | 變異位在遠處或其他染色體；效應小、需要大樣本 |
| eGene | 至少有一個顯著 cis-eQTL 的基因 |
| lead variant | 一個 QTL 訊號中最顯著的變異 |

常用工具：tensorQTL（GPU 加速）、QTLtools、FastQTL、MatrixEQTL；連鎖定位用 R/qtl。

## 相關統計方法

| 步驟 | 統計問題 | 筆記 |
| --- | --- | --- |
| 校正族群結構 | genotype PCs 當共變數，避免族群分層造成假關聯 | [PCA](../../../data-science/statistics/multivariate-analysis/pca.md)、[干擾與偏誤](../../../data-science/statistics/experimental-design/confounding-bias.md) |
| 親緣 / 重複量測 | 個體間不獨立 → 線性混合模型（kinship 當隨機效應，如 GEMMA、BOLT-LMM） | [混合效應模型](../../../data-science/statistics/regression-analysis/mixed-effects-models.md) |
| 表現量當 phenotype | 計數要先轉換（log / inverse normal），或用計數模型 | [GLM 計數模型](../../../data-science/statistics/regression-analysis/glm-count-models.md) |
| 檢定上百萬個 variant × 數萬個基因 | genome-wide 門檻（5 × 10⁻⁸）或 permutation / FDR | [多重檢定](../../../data-science/statistics/inferential-statistics/multiple-testing.md) |

各類分子 QTL 見 [eQTL](eqtl.md)、[sQTL](sqtl.md)、[pQTL](pqtl.md)；與 GWAS 整合見 [Colocalization](colocalization.md)。
