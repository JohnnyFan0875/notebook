[基因體學](../README.md) › [全基因體分析](README.md) › pQTL

# 蛋白質 QTL (Protein QTL, pQTL)

與蛋白質濃度（多為血漿蛋白）相關的遺傳變異。蛋白質比 mRNA 更接近功能與藥物標的，pQTL 常用於藥物標的排序與孟德爾隨機化。

| 平台 | 原理 | 規模 | 注意 |
| --- | --- | --- | --- |
| SomaScan（aptamer） | 修飾核酸適體結合蛋白 | ~7,000–11,000 種蛋白 | **cis-pQTL 可能是假象**：變異改變蛋白質上的結合表位，影響的是「偵測」而不是濃度 |
| Olink（PEA） | 成對抗體 + DNA 延伸 | ~3,000–5,000 種 | 同樣有表位效應的可能；與 SomaScan 結果相關性依蛋白而異 |
| 質譜 (MS) | 胜肽定量 | 數百–數千種 | 不受抗體表位影響，但血漿動態範圍大、低濃度蛋白難測 |

| 用途 | 說明 |
| --- | --- |
| 補充 eQTL | 轉錄與蛋白效應可能不同（轉譯調控、蛋白穩定性） |
| 標的排序 | GWAS 位點與 cis-pQTL [colocalization](colocalization.md)，支持某蛋白是致病媒介 |
| 孟德爾隨機化 | 以 cis-pQTL 當工具變數，推估提高 / 降低某蛋白對疾病的因果效應 |

> 判讀 cis-pQTL 時，檢查變異是否為改變蛋白序列的錯義變異；若是，要考慮表位假象，並用另一個平台或質譜交叉驗證。

統計框架（族群結構 PCs、多重檢定）同 eQTL，見 [QTL 分析：相關統計方法](qtl-analysis-and-mapping.md#相關統計方法)。大型資源：UK Biobank Pharma Proteomics Project（見 [UK Biobank](../../clinical-informatics-and-standards/clinical-databases/uk-biobank.md)）、deCODE。
