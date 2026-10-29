# QTL Analysis and Mapping

QTL mapping links genetic variation to quantitative traits such as expression, protein abundance, metabolite levels, or organismal phenotypes.

## Workflow

- Define phenotype and genotype inputs
- Test associations across loci
- Correct for multiple testing and covariates
- Interpret peaks and candidate genes

## Variants of the Approach

- Linkage-based mapping
- Association-based mapping
- Fine-mapping after locus discovery

## 相關統計方法

| 步驟 | 統計問題 | 筆記 |
| --- | --- | --- |
| 校正族群結構 | genotype PCs 當共變數，避免族群分層造成假關聯 | [PCA](../../../data-science/statistics/multivariate-analysis/pca.md)、[干擾與偏誤](../../../data-science/statistics/experimental-design/confounding-bias.md) |
| 親緣 / 重複量測 | 個體間不獨立 → 線性混合模型（kinship 當隨機效應，如 GEMMA、BOLT-LMM） | [混合效應模型](../../../data-science/statistics/regression-analysis/mixed-effects-models.md) |
| 表現量當 phenotype | 計數要先轉換（log / inverse normal），或用計數模型 | [GLM 計數模型](../../../data-science/statistics/regression-analysis/glm-count-models.md) |
| 檢定上百萬個 variant × 數萬個基因 | genome-wide 門檻（5 × 10⁻⁸）或 permutation / FDR | [多重檢定](../../../data-science/statistics/inferential-statistics/multiple-testing.md) |
