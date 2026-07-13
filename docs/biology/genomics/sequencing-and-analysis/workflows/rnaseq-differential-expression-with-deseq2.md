# RNA-seq Differential Expression with DESeq2

這份 workflow 的核心不是「把 counts 丟進一個函式」，而是先把 RNA-seq 的 count matrix、sample metadata、normalization、探索性視覺化與 differential expression testing 串成一條有檢查點的流程。

`DESeq2` 最適合的情境是：你有原始或 feature-level gene counts，想做 count-aware 的差異表達分析，而不是直接把 TPM / FPKM 當成一般連續值建模。

## Core Mental Model

一條常見的 `DESeq2` workflow 可以先記成：

1. 準備 raw count matrix
2. 對齊 sample metadata 與 count columns
3. 建立 `DESeqDataSet`
4. 做 size-factor normalization
5. 用 `vst()` 或 `rlog()` 做探索性轉換
6. 用 heatmap / PCA 檢查 sample-level structure
7. 執行 `DESeq()`
8. 用 `results()` 與 `lfcShrink()` 取回可解讀的 differential expression 結果

Key point: `DESeq2` 不是只負責最後的 p-value，它也提供 count-aware normalization 與 sample-level exploratory views。

## Why Raw Counts Matter

RNA-seq counts 不是一般連續資料。它們通常：

- 非負整數
- heavily skewed
- variance 隨平均表達量改變
- library size 不同時不能直接拿來比較

因此第一個原則是：差異表達的主分析應從 raw counts 出發。

如果你只有 TPM / FPKM，這些值比較適合描述表達量或做某些 exploratory plots，不適合直接替代 count-based DE testing。

## Start from a Count Matrix and Metadata

`DESeq2` 的起點通常是一個 gene-by-sample count matrix，加上一份 sample metadata：

```r
dds <- DESeqDataSetFromMatrix(
  countData = rawcounts,
  colData = metadata,
  design = ~ condition
)
```

這裡最重要的不是函式名，而是兩個對齊條件：

- `countData` 的欄順序必須對應 `metadata` 的 sample 順序
- `design = ~ condition` 必須反映你真正要比較的生物條件

如果 sample annotation 沒有先對齊，再精緻的下游分析都會建立在錯誤配對上。

## Normalization with Size Factors

不同 sample 的測序深度不一樣，所以 raw counts 不能直接橫向比較。`DESeq2` 先估計 size factors：

```r
dds <- estimateSizeFactors(dds)
sizeFactors(dds)
```

接著可以取出 normalized counts：

```r
normalized_counts <- counts(dds, normalized = TRUE)
```

這一步的意義是讓 sample 間的 count scale 可比較，但要注意：

- normalized counts 方便檢查與視覺化
- 主分析本身仍是由 `DESeq()` 在模型裡完成，不是手動拿 normalized counts 去跑 t-test

## Exploratory Transformation: `vst()` or `rlog()`

raw counts 與 normalized counts 仍然常呈現 mean-dependent variance，所以做 sample clustering 或 PCA 時，通常會先做 variance-stabilizing transformation：

```r
vsd <- vst(dds, blind = TRUE)
```

或在某些資料量較小的情境使用 `rlog()`。

這類轉換的目的不是取代主分析，而是讓樣本層級視覺化更穩定：

- sample-to-sample distances
- hierarchical clustering
- PCA
- heatmaps

Key point: `vst()` 常是為了 exploratory structure，不是為了直接替換 `DESeq()` 的 count model。

## Sample-Level QC with Correlation Heatmaps

做完 `vst()` 後，常見的第一步是看 sample correlation：

```r
vsd_mat <- assay(vsd)
vsd_cor <- cor(vsd_mat)

library(pheatmap)
pheatmap(vsd_cor, annotation = metadata[, "condition", drop = FALSE])
```

這能幫你快速檢查：

- replicate 是否聚在一起
- 不同 condition 是否大致分開
- 是否有明顯 outlier sample
- technical effect 是否蓋過 biological effect

如果相關結構完全不符合實驗設計，應先停下來檢查 metadata、batch effect 或 sample quality。

## PCA for Sample Structure

`DESeq2` 也內建 sample-level PCA 視圖：

```r
plotPCA(vsd, intgroup = "condition")
```

PCA 在 RNA-seq workflow 的主要用途不是降維本身，而是問：

- 主要變異來源是不是你關心的 condition
- replicate 是否穩定
- batch / treatment / genotype 哪個在驅動分離

如果 PC1 / PC2 完全由未知技術因素主導，直接解讀差異表達會很危險。

## Running the Main DESeq2 Model

建立好 `DESeqDataSet` 後，主分析通常是一行：

```r
dds <- DESeq(dds)
```

這一步會把 `DESeq2` 的主要估計流程串起來，包括：

- normalization information
- dispersion estimation
- negative-binomial model fitting

你也可以用 `plotDispEsts(dds)` 看 dispersion fit 是否合理：

```r
plotDispEsts(dds)
```

這是一個很好的 sanity check，因為 RNA-seq differential expression 的穩定性，很大程度仰賴 dispersion modeling。

## Extracting Differential Expression Results

完成模型後，用 `results()` 取回特定對比：

```r
res <- results(dds, alpha = 0.05)
```

若要指定某個條件比較：

```r
res <- results(dds, contrast = c("condition", "treated", "control"))
```

這裡最值得確認的是：

- 參考組是誰
- log2 fold change 的方向怎麼定義
- `padj` 是否是你真正要用來篩選的欄位

很多解讀錯誤不是統計問題，而是把 contrast 方向看反了。

## Shrinking Log Fold Changes

RNA-seq 裡低 count feature 的 fold change 往往不穩定，所以 `DESeq2` 常配合 `lfcShrink()`：

```r
res_shrunk <- lfcShrink(dds, coef = 2, res = res)
```

這麼做的目的不是讓結果「看起來比較保守」，而是讓 log fold change 在低資訊區域更穩定、更適合排序與視覺化。

這在 MA plot、gene ranking 與 downstream interpretation 特別重要。

## Visualizing DE Results

最常見的一個結果圖是 MA plot：

```r
plotMA(res_shrunk, ylim = c(-8, 8))
```

MA plot 幫你同時看：

- 平均表達量
- log2 fold change
- 哪些基因在高 / 低 expression 區域出現明顯偏移

如果想看顯著基因在樣本間的 pattern，也常直接用 normalized counts 做 heatmap：

```r
sig_norm_counts <- normalized_counts[rownames(res_shrunk)[which(res_shrunk$padj < 0.05)], ]

pheatmap(
  sig_norm_counts,
  annotation = metadata[, "condition", drop = FALSE],
  scale = "row"
)
```

這不是正式統計檢定的一部分，但很有助於確認顯著基因是不是呈現一致的 sample-level pattern。

## Practical Interpretation Habits

- 先看 sample clustering / PCA，再看 gene-level p-values。
- 先確認 contrast 方向，再解讀 log2 fold change。
- 用 `normalized=TRUE` 的 counts 做展示與檢查，但主分析仍交給 `DESeq2` 模型。
- 低 count 基因的 effect size 先考慮 shrinkage，再做排序或視覺化。
- 如果 sample structure 被 batch 主導，先回頭修正設計，而不是急著列顯著基因名單。

## Common Mistakes

- metadata 與 count matrix 欄位順序沒有對齊
- 直接拿 TPM / FPKM 當 `DESeq2` 輸入
- 把 normalized counts 當成主檢定資料，自己外接不適合的統計方法
- 沒做 `vst()` / PCA / heatmap 就直接相信 differential expression 結果
- 忘記 shrinkage 後的 fold change 會比原始估計更適合解讀與排序

## Relation to Other Bioconductor Workflows

- 如果你想先理解 Bioconductor 的共同物件系統，先看 [Introduction to Bioconductor](bioconductor-introduction.md)。
- 如果你處理的是 array-oriented expression workflow，或需要線性模型 / 對比矩陣語言，對照看 [Differential Expression with limma](limma-differential-expression.md)。

可以把兩者先粗略分工成：

- `DESeq2`: count-based RNA-seq differential expression
- `limma`: 線性模型式 differential expression 與更一般的對比設計語言
