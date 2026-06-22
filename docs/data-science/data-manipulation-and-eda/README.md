# Data Manipulation and EDA

這個章節放在建模之前，目的是先把資料看懂。很多機器學習或統計分析的失敗，其實不是模型選錯，而是太早跳進建模，沒有先處理欄位定義、缺失值、重複值、異常值與資料分布。

## 建議閱讀順序

1. [EDA Workflow](eda-workflow.md): 建立一套固定的資料盤點與探索節奏。
2. [Data Profiling](data-profiling.md): 學會快速看懂資料型態、品質與欄位風險。
3. [Cohort Analysis](cohort-analysis.md): 用 cohort table 與 retention heatmap 追蹤群組隨時間的變化。
4. [Missing Data](missing-data.md): 釐清缺失值成因、處理策略與常見誤區。
5. [Visualization](visualization/README.md): 把 EDA 的發現轉成可比較、可溝通的圖表。

## 這一章要解決什麼

- 我拿到的新資料集，第一步該看什麼？
- 哪些欄位有資料品質風險，會影響後面分析？
- 如果是 user / customer data，要怎麼拆 cohort 才看得出 retention 變化？
- 缺失值到底要刪掉、填補，還是先保留並記錄？
- 圖表與摘要統計要如何搭配，避免只看平均數就下結論？

## 與其他章節的銜接

- 欄位整理與索引操作可搭配 [pandas](../python-foundations/pandas/README.md)。
- 視覺化探索已整合到本章的 [Visualization](visualization/README.md) 子章節。
- 當資料品質確認後，再進入 [Statistics](../statistics/README.md) 或 [Machine Learning](../machine-learning/README.md)。
