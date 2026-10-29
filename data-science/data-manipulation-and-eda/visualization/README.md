[Data Science](../../README.md) › [資料處理與 EDA](../README.md) › 視覺化

# 視覺化 (Visualization)

把分析問題轉成讀者看得懂的證據。先學設計原則，再學工具：Matplotlib 是底層，Seaborn 與 pandas `.plot()` 都建立在它之上。

```text
設計原則 → Matplotlib（figure / axes）→ Seaborn（統計圖）→ pandas plotting（快速檢查、時間序列）
                                    R：ggplot2（圖形文法）
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [圖表設計原則](chart-design-principles.md) | 選圖、常見誤導、顏色、出版輸出 | 這個問題該畫什麼圖？怎麼不誤導？ |
| [Matplotlib](matplotlib/README.md) | figure / axes、各種圖型、雙軸、註解 | 怎麼精確控制每個元素？ |
| [Seaborn](seaborn/README.md) | 分布、類別、關係、迴歸、矩陣圖 | 怎麼從 DataFrame 快速畫統計圖？ |
| [pandas Plotting](pandas-plotting.md) | `df.plot()`、時間序列的 rolling / resample 圖 | 怎麼最快看一眼資料？ |
| [ggplot2](ggplot2.md) | 圖形文法、geom 選擇、volcano / PCA、`coord_cartesian` vs `limits`、Python 對照 | 在 R 裡怎麼畫出版級的圖？ |

## 選工具

| 工具 | 最適合 | 注意 |
| --- | --- | --- |
| pandas `.plot()` | 第一眼檢查、時間序列 | 客製化有限 |
| Seaborn | EDA、分組比較、統計圖（自動算平均與 CI） | 細節仍要用 Matplotlib 的 `ax` 調整 |
| Matplotlib | 多子圖版面、出版級控制、特殊圖 | 語法較冗長 |
| ggplot2（R） | 分組、分面、出版級統計圖 | 資料要先整理成長表 |

## 選圖速查

| 問題 | 首選 | 替代 / 補充 |
| --- | --- | --- |
| 類別大小比較 | 排序長條圖 | 點圖 (dot plot)；避免圓餅圖 |
| 單一連續變數分布 | histogram、KDE | ECDF（不受 bin 影響） |
| 各組分布比較 | box + 原始點、violin | strip / swarm（n 小時） |
| 兩個連續變數 | scatter | n 很大用 hexbin / 2D density |
| 時間趨勢 | line | rolling mean、small multiples |
| 多變數關係 | pairplot、相關 heatmap | PCA 圖、clustermap |
| 差異表現結果 | volcano plot、MA plot | 見 [RNA-seq 對比與視覺化](../../../biology/genomics/sequencing-and-analysis/workflows/rna-seq/08-contrasts-testing-and-visualization.md) |

| 相關 | 連結 |
| --- | --- |
| 把圖組成儀表板 | [Dashboard Design](../../data-communication/dashboard-design.md) |
| 分布、效果量的統計意義 | [Statistics](../../statistics/README.md) |
| 模型評估圖（ROC、校準、殘差） | [ML Evaluation](../../machine-learning/evaluation/README.md)、[Interpretability](../../machine-learning/interpretability-and-diagnostics/README.md) |
| R 的作圖 | [ggplot2](ggplot2.md)、[tidyverse：接到 ggplot2](../../r-foundations/tidyverse-workflow.md#接到-ggplot2) |
