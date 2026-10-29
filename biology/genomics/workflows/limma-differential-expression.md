[基因體學](../README.md) › [分析流程](README.md) › limma

# limma 差異表現分析 (Differential Expression with limma)

limma 對每個基因擬合同一個線性模型，再用經驗貝氏 (empirical Bayes) 借用所有基因的資訊穩定變異估計。它源自 microarray，現在也用於 RNA-seq（voom）、蛋白質體、甲基化等連續型資料。**差異表現主要是設計問題**：設計矩陣與對比寫對了，檢定就很直接。RNA-seq 的 voom 用法見 [RNA-seq 07](rna-seq/07-differential-expression.md#limma-voom)。

> 以下程式碼以 limma 3.68 在模擬表現矩陣上驗證 API；`eset` 是 Biobase 的 ExpressionSet（`exprs()` 取矩陣、`pData()` 取樣本資訊），一般矩陣也可直接使用。

## 流程

```
檢查分布 → log2 轉換 → 標準化 → 過濾低訊號 → MDS 看樣本結構
  → 設計矩陣 → 對比 → lmFit → contrasts.fit → eBayes → decideTests / topTable → 視覺化、基因集
```

```r
library(limma)

# 1. 前處理（microarray）
plotDensities(eset, legend = FALSE)                       # 樣本分布是否對齊、有無離群樣本
exprs(eset) <- log2(exprs(eset))                          # 乘法差異 → 加法差異；limma 慣用 log2
exprs(eset) <- normalizeBetweenArrays(exprs(eset))        # quantile 標準化：讓各樣本分布一致
eset <- eset[rowMeans(exprs(eset)) > 5, ]                 # 移除接近背景值的探針（閾值依平台）

# 2. 樣本結構
plotMDS(eset, labels = pData(eset)$treatment, gene.selection = "common")

# 3. 模型
design <- model.matrix(~ 0 + er, data = pData(eset))      # 無截距：每組一個平均值
cm <- makeContrasts(status = erpositive - ernegative, levels = design)
fit  <- lmFit(eset, design)                               # 每個基因的係數
fit2 <- eBayes(contrasts.fit(fit, contrasts = cm))        # 轉成對比 + 收縮標準誤
summary(decideTests(fit2))                                # 上調 / 下調 / 不顯著的基因數
topTable(fit2, coef = "status", number = 10)              # logFC、AveExpr、t、P.Value、adj.P.Val、B
```

| 函式 | 作用 |
| --- | --- |
| `lmFit()` | 每個基因估計設計矩陣的係數 |
| `contrasts.fit()` | 把係數改寫成要比較的對比 |
| `eBayes()` | 經驗貝氏：每個基因的變異往所有基因的共同趨勢收縮 → moderated t，小樣本也穩定 |
| `decideTests()` | 依閾值統計各對比的顯著基因數 |
| `topTable()` | 單一對比的完整結果表（`number = Inf` 取全部） |

> quantile 標準化是 microarray 的標準做法，但會破壞 RNA-seq counts 的平均–變異關係，**不要用在 RNA-seq counts 上**；RNA-seq 用 TMM + voom。

## 設計矩陣與對比

| 寫法 | 係數意義 | 適合 |
| --- | --- | --- |
| `~ er` | 截距 = 參考組平均；`erpositive` = 兩組差 | 單純兩組 |
| `~ 0 + er` | 每組各自的平均 | 自訂多個對比 |
| `~ 0 + group + batch` | 組平均 + 批次效應 | 批次納入模型 |

一次擬合、多個問題：

```r
# 多組
cm <- makeContrasts(AMLvALL = typeAML - typeALL,
                    CMLvALL = typeCML - typeALL,
                    CMLvAML = typeCML - typeAML, levels = design)

# 2 × 2 因子設計：把兩個因子合成一個 group
group  <- factor(with(pData(eset), paste(genotype, treatment, sep = ".")))
design <- model.matrix(~ 0 + group); colnames(design) <- levels(group)
cm <- makeContrasts(
  dox_wt      = wt.dox - wt.pbs,                                   # 野生型對藥物的反應
  dox_top2b   = top2b.dox - top2b.pbs,                             # 突變型對藥物的反應
  interaction = (top2b.dox - top2b.pbs) - (wt.dox - wt.pbs),       # 反應是否因基因型而不同
  levels = design)
```

交互作用的解讀（差異中的差異）見 [RNA-seq 08：交互作用](rna-seq/08-contrasts-testing-and-visualization.md#交互作用與差異中的差異)。

## 批次效應

| 做法 | 用途 |
| --- | --- |
| 批次放進設計矩陣（`~ 0 + group + batch`） | **正式檢定**的建議做法 |
| `removeBatchEffect(x, batch = , covariates = , group = )` | 只用於視覺化（PCA、熱圖）；不要拿校正後的資料再做檢定 |
| `duplicateCorrelation()` + `block =` | 同一受試者多個樣本（重複量測） |

批次與組別完全重疊時無法分離，見 [干擾與偏誤](../../../data-science/statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)。

## 診斷與視覺化

| 圖 | 函式 | 看什麼 |
| --- | --- | --- |
| 密度圖 | `plotDensities()` | 前處理是否讓樣本分布一致 |
| MDS | `plotMDS()` | 主要變異是否來自實驗條件 |
| p 值直方圖 | `hist(fit2$p.value[, "status"])` | 左側尖峰 + 平坦 = 有訊號且模型合理（見 [多重檢定：p 值直方圖](../../../data-science/statistics/inferential-statistics/multiple-testing.md#診斷p-值直方圖)） |
| Volcano | `volcanoplot(fit2, coef = , highlight = 5, names = )` | 效果量 vs 顯著性 |
| MA / mean-difference | `plotMD(fit2)` | 效果量 vs 平均表現量 |

## 基因集檢定

| 函式 | 問題 | 特點 |
| --- | --- | --- |
| `camera()` | 這組基因整體是否比其他基因更常變化？（競爭型） | 考慮基因間相關，比一般 ORA 的型一錯誤控制好 |
| `roast()` / `mroast()` | 這組基因是否有變化？（自足型） | 旋轉檢定，可看上調 / 下調比例 |
| `fry()` | roast 的快速近似 | 大量基因集 |

```r
idx <- ids2indices(gene_sets, rownames(eset))    # 基因集 → 列索引
camera(eset, idx, design, contrast = cm[, "status"])
```

ORA / GSEA 見 [RNA-seq 09](rna-seq/09-annotation-and-functional-enrichment.md)。統計背景：[GLM 與線性模型](../../../data-science/statistics/regression-analysis/README.md)、[多重檢定](../../../data-science/statistics/inferential-statistics/multiple-testing.md)。
