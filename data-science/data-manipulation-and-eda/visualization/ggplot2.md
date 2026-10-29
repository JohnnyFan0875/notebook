[資料處理與 EDA](../README.md) › [視覺化](README.md) › ggplot2

# ggplot2

R 的標準作圖套件，依「圖形文法 (grammar of graphics)」把圖拆成資料、映射、幾何物件、尺度、分面、主題等圖層，用 `+` 疊起來。Python 的對應是 Seaborn（快速統計圖）+ Matplotlib（細節）；plotnine 則是 ggplot2 語法的 Python 移植。

## 圖形文法

| 元件 | 函式 | 作用 |
| --- | --- | --- |
| 資料 | `ggplot(df)` | **長表**（tidy）：一列一個觀測 |
| 映射 (aesthetics) | `aes(x, y, color, fill, shape, size, group)` | 欄位 → 視覺屬性 |
| 幾何物件 | `geom_*()` | 點、線、長條、箱形… |
| 統計轉換 | `stat_*()` / geom 內建 | 計數、密度、平滑、摘要 |
| 尺度 | `scale_*()` | 軸轉換（log）、顏色盤、標籤 |
| 分面 | `facet_wrap()` / `facet_grid()` | small multiples |
| 座標 | `coord_*()` | 縮放、翻轉、比例 |
| 主題 | `theme_*()`、`theme()` | 字型、背景、圖例位置 |

```r
library(ggplot2)

ggplot(df, aes(x = dose, y = response, color = genotype)) +   # 資料 + 映射
  geom_point(alpha = 0.6) +                                   # 原始點
  geom_smooth(method = "lm", se = TRUE) +                     # 每組一條迴歸線 + 95% CI
  scale_x_log10() +                                           # 尺度
  facet_wrap(vars(cell_line)) +                               # 分面
  labs(x = "Dose (µM, log)", y = "Viability", color = NULL) +
  theme_bw(base_size = 12)
```

> **映射 vs 設定**：`aes(color = genotype)` 是依欄位上色並產生圖例；`geom_point(color = "red")` 是固定顏色。把固定值寫進 `aes(color = "red")` 會多出一個叫 "red" 的圖例，是最常見的錯誤。

## 依問題選 geom

| 問題 | geom | 注意 |
| --- | --- | --- |
| 單變數分布 | `geom_histogram(bins = 30)`、`geom_density()` | 一定要試不同 `bins` / `binwidth` |
| 組間分布比較 | `geom_boxplot(outlier.shape = NA) + geom_jitter(width = 0.2)` | n 小時一定要畫原始點；`geom_violin()` 看形狀 |
| 平均 ± 誤差 | `stat_summary(fun.data = mean_cl_normal)` | 需 Hmisc；或先 `summarise()` 再 `geom_pointrange()` |
| 兩連續變數 | `geom_point()`；點很多用 `geom_hex()` / `geom_bin_2d()` | |
| 趨勢 / 時間 | `geom_line(aes(group = id))` | 重複量測要指定 `group` 才不會連錯 |
| 類別計數 | `geom_bar()`（自動數）/ `geom_col()`（已有數值） | |
| 矩陣 / heatmap | `geom_tile(aes(fill = value))` | 需分群排序時改用 `pheatmap` / `ComplexHeatmap` |
| 標註 | `annotate()`、`geom_text()`、`ggrepel::geom_text_repel()` | 標籤重疊用 ggrepel |

`geom_*` 的計算欄位用 `after_stat()`：`geom_histogram(aes(y = after_stat(density)))`（舊寫法 `..density..` 已棄用）。線條粗細從 3.4.0 起用 `linewidth`（不是 `size`）。

## 生資常見圖

```r
library(ggplot2); library(dplyr)

# 1. 表現量：箱形 + 原始點（先 pivot_longer 成長表）
expr_long |>
  filter(gene %in% c("TP53", "MYC")) |>
  ggplot(aes(condition, log2_cpm, fill = condition)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.5) +
  geom_jitter(width = 0.15, size = 1.5) +
  facet_wrap(vars(gene), scales = "free_y") +
  theme_bw() + theme(legend.position = "none")

# 2. Volcano plot：DESeq2 結果
res_df |>
  mutate(sig = padj < 0.05 & abs(log2FoldChange) > 1) |>
  ggplot(aes(log2FoldChange, -log10(pvalue), color = sig)) +
  geom_point(size = 0.8, alpha = 0.6) +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed") +
  scale_color_manual(values = c(`FALSE` = "grey70", `TRUE` = "firebrick")) +
  ggrepel::geom_text_repel(data = \(d) slice_min(d, padj, n = 10), aes(label = gene),
                           color = "black", size = 3)

# 3. PCA：樣本著色 = 條件、形狀 = 批次（檢查批次效應）
pca <- prcomp(t(vst_mat))
pct <- round(100 * pca$sdev^2 / sum(pca$sdev^2), 1)
cbind(sample_info, pca$x[, 1:2]) |>
  ggplot(aes(PC1, PC2, color = condition, shape = batch)) +
  geom_point(size = 3) +
  labs(x = paste0("PC1 (", pct[1], "%)"), y = paste0("PC2 (", pct[2], "%)")) +
  coord_fixed()                                     # 兩軸同比例，距離才可比較
```

Volcano / MA plot 的判讀見 [RNA-seq 對比與視覺化](../../../biology/genomics/sequencing-and-analysis/workflows/rna-seq/08-contrasts-testing-and-visualization.md)；PCA 見 [PCA](../../statistics/multivariate-analysis/pca.md)。

## 尺度、顏色、分面

| 需求 | 寫法 |
| --- | --- |
| log 軸 | `scale_x_log10()`、`scale_y_continuous(trans = "log2")` |
| 百分比 / 千分位標籤 | `scale_y_continuous(labels = scales::percent)`、`scales::comma` |
| 類別顏色 | `scale_color_brewer(palette = "Set2")`、`scale_color_manual(values = c(a = "steelblue", b = "tomato"))` |
| 連續顏色（色盲友善） | `scale_fill_viridis_c()` |
| 發散色（log2FC、z-score） | `scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)` |
| 類別順序 | 改資料：`mutate(cond = forcats::fct_relevel(cond, "control"))`、`fct_reorder(gene, value)` |
| 每格獨立 y 軸 | `facet_wrap(vars(gene), scales = "free_y")` |
| 兩個分類變數排成網格 | `facet_grid(rows = vars(tissue), cols = vars(time))` |
| 水平長條 | 直接 `aes(x = value, y = category)`（不必 `coord_flip()`） |

| 縮放方式 | 效果 |
| --- | --- |
| `coord_cartesian(ylim = c(0, 10))` | 只放大視窗，**所有資料仍參與計算** |
| `ylim(0, 10)` / `scale_y_continuous(limits = ...)` | **超出範圍的資料被刪掉**（變 NA）再計算 → 箱形圖、平滑線會改變 |

> 想「放大看」一定用 `coord_cartesian()`；用 `limits` 裁掉資料後，箱形圖的中位數和四分位數會跟著變，而且只留下一行警告。

## 主題與輸出

```r
theme_set(theme_bw(base_size = 12))                 # 全域預設主題

p <- last_plot() +
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust = 1),
        panel.grid.minor = element_blank())

ggsave("fig1.pdf", p, width = 180, height = 120, units = "mm")        # 向量圖：投稿首選
ggsave("fig1.png", p, width = 7, height = 5, dpi = 300)               # 點陣圖
```

| 需求 | 套件 |
| --- | --- |
| 多張圖拼版（A、B、C 標籤） | `patchwork`：`(p1 \| p2) / p3 + plot_annotation(tag_levels = "A")` |
| 標籤不重疊 | `ggrepel` |
| 顯著性標記 | `ggpubr::stat_compare_means()`（註明用的是哪個檢定與是否校正） |
| 複雜 heatmap | `pheatmap`、`ComplexHeatmap`（Bioconductor） |
| 互動 | `plotly::ggplotly(p)` |
| 迴圈 / 函式內作圖 | `aes({{ x }})` 搭配 tidy evaluation，見 [dplyr 程式化](../../r-foundations/dplyr-programming-patterns.md#包-ggplot2) |

## 與 Python 對照

| ggplot2 | Seaborn / Matplotlib | plotnine |
| --- | --- | --- |
| `ggplot(df, aes(x, y, color = g)) + geom_point()` | `sns.scatterplot(df, x=, y=, hue="g")` | 幾乎相同語法 |
| `geom_boxplot()` + `geom_jitter()` | `sns.boxplot()` + `sns.stripplot()` | 相同 |
| `facet_wrap(vars(g))` | `sns.relplot(..., col="g", col_wrap=3)` | `facet_wrap("g")` |
| `geom_smooth(method = "lm")` | `sns.regplot()` / `lmplot()` | `geom_smooth(method="lm")` |
| `theme_bw()` | `sns.set_theme(style="whitegrid")` | `theme_bw()` |
| `ggsave()` | `fig.savefig(dpi=, bbox_inches="tight")` | `p.save()` |

相關：[圖表設計原則](chart-design-principles.md)、[Seaborn](seaborn/README.md)、[tidyverse：接到 ggplot2](../../r-foundations/tidyverse-workflow.md#接到-ggplot2)、[tidyr 長寬轉換](../../r-foundations/data-reshaping-with-tidyr.md)。
