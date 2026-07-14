# Visualization

資料視覺化不是把數字畫成圖而已，而是把分析問題轉成讀者能理解的證據。這個章節把常用的 Python 繪圖工具與圖表設計原則整理成一條可實作的路線。

## 建議閱讀順序

1. [Chart Design Principles](chart-design-principles.md): 先理解圖表為什麼容易誤導，以及如何設計可讀的圖。
2. [Dashboard Design](dashboard-design.md): 當圖表不是單張輸出，而是要組成決策介面時，先理解 dashboard 編排原則。
3. [Matplotlib](matplotlib/README.md): 學會 figure、axes、標籤、版面與輸出控制。
4. [Seaborn](seaborn/README.md): 進一步處理統計圖、分組比較與高階語意映射。

## 何時用哪個工具

| 工具 | 最適合的場景 | 注意事項 |
| --- | --- | --- |
| [Matplotlib](matplotlib/README.md) | 客製化版面、多子圖、出版級控制 | 語法較底層，但最靈活 |
| [Seaborn](seaborn/README.md) | EDA、統計圖、直接吃 DataFrame | 高階 API 方便，但仍要理解底層軸設定 |

## 常見選圖原則

- 比較類別大小時，先想長條圖，不要先想圓餅圖。
- 看分布時，優先用 histogram、KDE、boxplot 或 violin plot。
- 看兩個連續變數關係時，先用 scatter plot，再判斷是否需要回歸線。
- 看時間變化時，優先用 line plot，並清楚標示時間刻度與單位。
- 看多個變數之間的整體關係時，可考慮 heatmap、pairplot 或 facet grid。

## 與其他章節的關係

- 需要資料清理與欄位整理時，先回到本章前面的 [Data Manipulation and EDA](../README.md)。
- 需要理解分布、假設檢定或效果量時，回到 [Statistics](../../statistics/README.md)。
- 需要用圖解釋模型結果時，參考 [Machine Learning Evaluation](../../machine-learning/evaluation/README.md) 與 [Interpretability and Diagnostics](../../machine-learning/interpretability-and-diagnostics/README.md)。
