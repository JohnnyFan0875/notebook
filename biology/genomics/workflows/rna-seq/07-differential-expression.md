[分析流程](../README.md) › [RNA-seq](README.md) › 07 差異表現

# 差異表現分析：edgeR、DESeq2、limma-voom (Differential Expression)

三個套件都能做嚴謹的 gene-level 差異表現 (DE) 分析，差別在標準化、變異建模與檢定方式。三者共同的前提：**輸入是 raw counts（或 tximport 的估計 counts），不是 TPM / FPKM**；樣本資訊與 count 欄位順序一致；設計矩陣反映真正要比較的條件。

本章的程式碼以 R 4.6.1 / edgeR 4.10、DESeq2 1.52、limma 3.68 在本系列的模擬資料（`data/`）上實跑；結果不代表真實生物學發現。完整腳本在 `scripts/`。

```r
library(readr)
counts_tbl <- read_csv("data/simulated_gene_counts.csv", show_col_types = FALSE)
metadata   <- read_csv("data/sample_metadata.csv", show_col_types = FALSE)
counts <- as.matrix(counts_tbl[, metadata$sample_id])      # 依 metadata 順序取欄
rownames(counts) <- counts_tbl$gene_id
metadata$group <- relevel(factor(metadata$group), ref = "control")   # 參考組決定 logFC 方向
```

## edgeR

負二項 GLM + TMM 標準化 + 經驗貝氏收縮 dispersion；建議用 quasi-likelihood (QL) F 檢定，對小樣本的型一錯誤控制較好。

```r
library(edgeR)
design <- model.matrix(~ group, data = metadata)

y <- DGEList(counts = counts, group = metadata$group)     # counts、library size、group
y <- y[filterByExpr(y, design), , keep.lib.sizes = FALSE] # 依設計過濾低表現基因
y <- normLibSizes(y, method = "TMM")                     # TMM 因子（edgeR < 4.0：calcNormFactors）
y <- estimateDisp(y, design)                             # common / trended / tagwise dispersion
fit <- glmQLFit(y, design)                               # QL 負二項 GLM
qlf <- glmQLFTest(fit, coef = "grouptreated")            # treated vs control
res_edger <- topTags(qlf, n = Inf)$table                 # logFC、logCPM、F、PValue、FDR
plotBCV(y); plotQLDisp(fit)                              # dispersion 診斷
```

## DESeq2

負二項 GLM + median-of-ratios size factor + dispersion 趨勢收縮；預設 Wald 檢定，另有 LRT 與 log fold change 收縮。

```r
library(DESeq2)
dds <- DESeqDataSetFromMatrix(round(counts), colData = metadata, design = ~ group)
dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]            # 預過濾（主要為了速度）
dds <- DESeq(dds)                                         # size factor → dispersion → GLM → Wald

sizeFactors(dds)                                          # 每個樣本的 size factor
counts(dds, normalized = TRUE)                            # 標準化 counts：只用於展示，不拿去另做 t 檢定
plotDispEsts(dds)                                         # dispersion 擬合是否合理
resultsNames(dds)                                         # "Intercept" "group_treated_vs_control"

res <- results(dds, contrast = c("group", "treated", "control"), alpha = 0.05)
summary(res)
res_shrunk <- lfcShrink(dds, coef = "group_treated_vs_control", type = "apeglm")
plotMA(res_shrunk, ylim = c(-4, 4))
```

| 步驟 | 為什麼 |
| --- | --- |
| median-of-ratios size factor | 以所有基因的幾何平均建「虛擬參考樣本」，取各樣本相對比值的中位數；同時校正定序深度與組成偏差 |
| `results(alpha = 0.05)` | 依目標 FDR 自動做獨立過濾 (independent filtering)，低表現基因的 `padj` 會是 `NA` |
| `lfcShrink()`（apeglm） | 低 count 基因的 LFC 估計很不穩，收縮後更適合**排序與作圖**；顯著性仍看 `results()` 的 `padj` |
| `vst()` | 探索性分析用，見 [06：VST 後再看樣本結構](06-exploratory-design-and-count-models.md#deseq2-的做法vst-後再看樣本結構) |

結果欄位：`baseMean`（平均標準化 counts）、`log2FoldChange`、`lfcSE`、`stat`、`pvalue`、`padj`。

## limma-voom

把 counts 轉成 log-CPM，由平均–變異趨勢為每個觀測值算 precision weight，再用 limma 的加權線性模型與經驗貝氏。設計彈性最大（批次、配對、複雜對比、樣本品質權重）。

```r
library(limma)
design <- model.matrix(~ 0 + group, data = metadata)      # 無截距：每組一欄
colnames(design) <- levels(metadata$group)

y <- DGEList(counts)
y <- y[filterByExpr(y, design), , keep.lib.sizes = FALSE]
y <- normLibSizes(y)
v <- voom(y, design, plot = TRUE)                         # 平均–變異趨勢 → precision weights
fit <- lmFit(v, design)
fit2 <- eBayes(contrasts.fit(fit, makeContrasts(treated - control, levels = design)))
res_limma <- topTable(fit2, number = Inf, sort.by = "P")  # logFC、AveExpr、t、P.Value、adj.P.Val
```

重複量測或同一病人多樣本：`duplicateCorrelation()` 或 `dream()`（variancePartition），概念同 [混合效應模型](../../../../data-science/statistics/regression-analysis/mixed-effects-models.md)；樣本品質不一時用 `voomWithQualityWeights()`。

## 方法比較

| | edgeR | DESeq2 | limma-voom |
| --- | --- | --- | --- |
| 標準化 | TMM / TMMwsp | median-of-ratios | TMM + voom 權重 |
| 變異建模 | NB dispersion + 經驗貝氏 | NB dispersion 趨勢 + 收縮 | 平均–變異 precision weight |
| 檢定 | QL F、LRT、exact | Wald、LRT | moderated t / F |
| 強項 | 小樣本、QL 推論穩健 | 流程完整、LFC 收縮、診斷圖多 | 複雜設計、速度、與 limma 生態整合 |
| 結果欄位 | `logFC`、`logCPM`、`PValue`、`FDR` | `baseMean`、`log2FoldChange`、`pvalue`、`padj` | `logFC`、`AveExpr`、`P.Value`、`adj.P.Val` |
| 樣本數很少（n = 2–3） | 適合 | 適合 | 需要足夠樣本估平均–變異趨勢 |

在本系列模擬資料上（約 1,150 個通過過濾的基因），FDR < 0.05 的基因數為 edgeR 45、DESeq2 57、limma-voom 25。三者的顯著清單不必完全相同，差異來自過濾、標準化、變異建模、對比與多重檢定；**排名靠前的基因通常高度重疊**（本例 edgeR 與 limma-voom 的前 20 名有 18 個相同），邊界上的基因才有出入。

| 統計概念 | 對應筆記 |
| --- | --- |
| NB-GLM、log link、size factor 當 offset | [GLM 計數模型：RNA-seq 差異表現](../../../../data-science/statistics/regression-analysis/glm-count-models.md#生資應用rna-seq-差異表現) |
| `padj` / `FDR` / `adj.P.Val`（BH） | [多重檢定](../../../../data-science/statistics/inferential-statistics/multiple-testing.md) |
| 批次、配對、重複量測 | [混合效應模型](../../../../data-science/statistics/regression-analysis/mixed-effects-models.md)、[干擾與偏誤](../../../../data-science/statistics/experimental-design/confounding-bias.md) |

## 常見錯誤

| 錯誤 | 後果 | 修正 |
| --- | --- | --- |
| metadata 與 count 欄位順序不一致 | 組別標籤套到錯的樣本，程式不會報錯 | `stopifnot(identical(colnames(counts), metadata$sample_id))` |
| 用 TPM / FPKM 當輸入 | 模型假設錯誤 | raw counts 或 tximport 匯入 |
| 拿標準化 counts 另外跑 t 檢定 | 忽略計數資料的平均–變異關係 | 交給 DE 套件的模型 |
| 參考組沒設定 | logFC 方向與預期相反 | `relevel()`；結果檢查 `resultsNames()` |
| 用未收縮的 LFC 排序 | 低表現基因的極端 LFC 排在前面 | `lfcShrink()` 後排序 |
| 只看 DE，沒先看 PCA / 相關熱圖 | 批次或樣本錯置被當成生物訊號 | 先做 [06 的 EDA](06-exploratory-design-and-count-models.md) |
| 組別與批次完全重疊 | 設計矩陣不滿秩，無法分離 | 只能靠實驗設計解決 |

對比方向、交互作用、多重檢定與結果視覺化見 [08](08-contrasts-testing-and-visualization.md)；microarray 或其他連續型資料的 limma 用法見 [limma 差異表現](../limma-differential-expression.md)。
