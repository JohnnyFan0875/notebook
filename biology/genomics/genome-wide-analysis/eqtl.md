[基因體學](../README.md) › [全基因體分析](README.md) › eQTL

# 表現量 QTL (Expression QTL, eQTL)

與基因表現量相關的遺傳變異。多數 GWAS 位點落在非編碼區，eQTL 是把它們連到「透過改變哪個基因的表現量起作用」的主要橋樑。

| 概念 | 說明 |
| --- | --- |
| cis-eQTL | 變異在基因附近（±1 Mb）；效應大、容易偵測，多數已知 eQTL 屬此類 |
| trans-eQTL | 變異在遠處或他條染色體；常透過轉錄因子間接作用，效應小 |
| 組織專一性 | 同一變異在不同組織效應不同；要用與疾病相關的組織 |
| 效應量 | 常以每個 ALT 等位基因造成的 log 表現量變化（slope / aFC）表示 |

## 分析要點

| 要點 | 說明 |
| --- | --- |
| 隱藏變異 | 表現量受批次、細胞組成等未測量因素影響；常用 PEER factors 或表現量 PCs 當共變數（類似批次效應校正，見 [干擾與偏誤](../../../data-science/statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)、[PCA](../../../data-science/statistics/multivariate-analysis/pca.md)） |
| 多重檢定 | 每個基因檢定許多 variant：先在基因內做 permutation 得到基因層級 p 值，再跨基因做 FDR（[多重檢定](../../../data-science/statistics/inferential-statistics/multiple-testing.md)） |
| 細胞組成 | bulk 組織的 eQTL 可能其實是「細胞比例 QTL」；單細胞 eQTL 可分辨細胞類型 |
| 等位基因專一表現 (ASE) | 在異型合子個體中比較兩個等位基因的表現量，內建對照、不受個體間差異影響 |

統計框架見 [QTL 分析：相關統計方法](qtl-analysis-and-mapping.md#相關統計方法)。

## 資源

| 資源 | 內容 |
| --- | --- |
| [GTEx](../../genetics/databases/functional-expression/gtex.md) | 約 50 種人體組織的 eQTL / sQTL，最常用的參考 |
| eQTLGen | 大樣本血液 eQTL（含 trans） |
| eQTL Catalogue | 統一重新分析的多個研究 |

與 GWAS 整合判斷是否共享致病變異，見 [Colocalization](colocalization.md)。
