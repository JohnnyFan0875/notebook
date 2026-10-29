# eQTL

Expression quantitative trait loci (eQTL) are genetic variants associated with gene expression levels.

## Concepts

- `cis-eQTL`: near the regulated gene
- `trans-eQTL`: affects distant genes
- Tissue specificity is often important

## Notes

- GTEx is a common reference resource.
- eQTL results are often integrated with GWAS for biological interpretation.
- 表現量先移除隱藏變異：常用 PEER factors 或表現量 PCs 當共變數（類似批次效應校正，見 [干擾與偏誤](../../../../data-science/statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)、[PCA](../../../../data-science/statistics/multivariate-analysis/pca.md)）。
- cis-eQTL 每個基因檢定多個 variant：先在基因內做 permutation 得到基因層級 p 值，再跨基因做 FDR（[多重檢定](../../../../data-science/statistics/inferential-statistics/multiple-testing.md)）。統計框架見 [QTL Analysis and Mapping](qtl-analysis-and-mapping.md#相關統計方法)。
