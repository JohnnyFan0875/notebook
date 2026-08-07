# Differential Expression: edgeR, DESeq2, and limma-voom

本章目的：以 edgeR、DESeq2 與 limma-voom 介紹 RNA-seq differential expression 的完整分析結構。三者都能做嚴謹的 gene-level DE，但 normalization、dispersion/mean-variance modeling 與 testing 細節不同。

本節使用模擬資料示範分析流程，結果不代表真實生物學研究發現。

## edgeR

edgeR 使用 negative binomial GLM，透過 TMM normalization、dispersion estimation 與 empirical Bayes shrinkage 穩定推論。現代 edgeR workflow 常建議使用 quasi-likelihood F-test。

輸入資料：

- raw gene counts 或 tximport estimated counts。
- sample metadata。
- design matrix。

完整 R script：

```r
library(readr)
library(edgeR)

counts_tbl <- read_csv("data/simulated_gene_counts.csv", show_col_types = FALSE)
metadata <- read_csv("data/sample_metadata.csv", show_col_types = FALSE)
counts <- as.matrix(counts_tbl[, metadata$sample_id])
rownames(counts) <- counts_tbl[[1]]

metadata$group <- relevel(factor(metadata$group), ref = "control")
design <- model.matrix(~ group, data = metadata)

y <- DGEList(counts = counts, group = metadata$group)
keep <- filterByExpr(y, design)
y <- y[keep, , keep.lib.sizes = FALSE]
y <- calcNormFactors(y, method = "TMM")
y <- estimateDisp(y, design)

fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef = "grouptreated")
res <- topTags(qlf, n = Inf)$table
```

程式碼逐段說明：

- `DGEList()` 建立 edgeR 物件，保存 counts、library size 與 group。
- `filterByExpr()` 根據 design 過濾低表現基因。
- `calcNormFactors()` 計算 TMM normalization factor。
- `estimateDisp()` 估 common、trended、tagwise dispersion。
- `glmQLFit()` 擬合 quasi-likelihood negative binomial GLM。
- `glmQLFTest()` 對指定 coefficient 做檢定。
- `topTags()` 回傳排序後結果表。

結果欄位通常包含 `logFC`、`logCPM`、`F`、`PValue`、`FDR`。`logFC` 方向取決於 coefficient 或 contrast。

優點：小樣本常用、TMM 成熟、QL framework 穩健、contrast 彈性高。限制：需要理解 design/contrast 與 count input；TPM 不可直接當 counts。

## DESeq2

DESeq2 使用 negative binomial GLM、median-of-ratios size factor、dispersion trend 與 Wald/LRT testing。它也提供 VST/rlog 供 EDA 使用。

完整 R script：

```r
library(readr)
library(DESeq2)

counts_tbl <- read_csv("data/simulated_gene_counts.csv", show_col_types = FALSE)
metadata <- read_csv("data/sample_metadata.csv", show_col_types = FALSE)
counts <- round(as.matrix(counts_tbl[, metadata$sample_id]))
rownames(counts) <- counts_tbl[[1]]

metadata$group <- relevel(factor(metadata$group), ref = "control")
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = metadata,
  design = ~ group
)

dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("group", "treated", "control"), alpha = 0.05)
```

LFC shrinkage：

```r
library(apeglm)
res_shrunk <- lfcShrink(dds, coef = "group_treated_vs_control", type = "apeglm")
```

程式碼逐段說明：

- `DESeqDataSetFromMatrix()` 建立 DESeq2 object。
- `DESeq()` 執行 size factor estimation、dispersion estimation、model fitting 與 Wald test。
- `results()` 取出指定 contrast。
- `lfcShrink()` 穩定低 count gene 的 log2 fold change，常用於排序與視覺化。

結果欄位包含 `baseMean`、`log2FoldChange`、`lfcSE`、`stat`、`pvalue`、`padj`。

優點：介面完整、診斷圖多、LFC shrinkage 成熟。限制：design confounding 仍無法解決；estimated counts 需正確匯入；非常複雜 design 要仔細檢查 coefficient names。

## limma-voom

limma-voom 將 count data 轉成 log-CPM，估計 mean-variance trend，為每個 observation 建立 precision weight，再使用 limma linear model 與 empirical Bayes。

完整 R script：

```r
library(readr)
library(edgeR)
library(limma)

counts_tbl <- read_csv("data/simulated_gene_counts.csv", show_col_types = FALSE)
metadata <- read_csv("data/sample_metadata.csv", show_col_types = FALSE)
counts <- as.matrix(counts_tbl[, metadata$sample_id])
rownames(counts) <- counts_tbl[[1]]

metadata$group <- factor(metadata$group, levels = c("control", "treated"))
design <- model.matrix(~ 0 + group, data = metadata)
colnames(design) <- sub("^group", "", colnames(design))

y <- DGEList(counts = counts)
y <- y[filterByExpr(y, design), , keep.lib.sizes = FALSE]
y <- calcNormFactors(y)

v <- voom(y, design, plot = TRUE)
fit <- lmFit(v, design)
contr <- makeContrasts(treated - control, levels = design)
fit2 <- contrasts.fit(fit, contr)
fit2 <- eBayes(fit2)
res <- topTable(fit2, number = Inf, sort.by = "P")
```

程式碼逐段說明：

- `voom()` 估 mean-variance trend 並產生 precision weights。
- `lmFit()` 擬合 weighted linear model。
- `contrasts.fit()` 套用 contrast matrix。
- `eBayes()` 使用 empirical Bayes 穩定 variance。
- `topTable()` 輸出結果。

優點：design 彈性強，對 batch、paired、複雜 contrast、quality weights 很方便。限制：需要合理 replicate 數估 mean-variance；不是直接 NB model。

## Method Comparison

| Method | Normalization | Variance modeling | Test | Strength | Typical result columns |
| --- | --- | --- | --- | --- | --- |
| edgeR | TMM/TMMwsp | NB dispersion + empirical Bayes | exact test, LRT, QLF | 小樣本與 QL inference | `logFC`, `logCPM`, `PValue`, `FDR` |
| DESeq2 | median-of-ratios | NB dispersion trend + shrinkage | Wald, LRT | 完整 workflow 與 LFC shrinkage | `baseMean`, `log2FoldChange`, `pvalue`, `padj` |
| limma-voom | TMM + voom weights | mean-variance precision weights | moderated t/F | 複雜設計與 linear-model ecosystem | `logFC`, `AveExpr`, `P.Value`, `adj.P.Val` |

Key point: 三者的顯著基因清單不必完全相同。差異通常來自 filtering、normalization、dispersion/variance modeling、contrast、LFC shrinkage 與 multiple testing。

