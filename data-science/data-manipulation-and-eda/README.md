# Data Manipulation and EDA

這個章節放在建模之前，目的是先把資料看懂。很多機器學習或統計分析的失敗，其實不是模型選錯，而是太早跳進建模，沒有先處理欄位定義、缺失值、重複值、異常值與資料分布。

## 建議閱讀順序

1. [EDA Workflow](eda-workflow.md): 先做 data profiling（型別、完整性、唯一性），再走固定的探索節奏。
2. [Missing Data](missing-data.md): 缺失機制（MCAR / MAR / MNAR）與刪除策略；工具用法見 [pandas](../python-foundations/pandas/missing-data.md) / [R](../r-foundations/missing-data.md)，插補見 [Imputation](../machine-learning/preprocessing/imputation.md)。
3. [Visualization](visualization/README.md): 把 EDA 的發現轉成可比較、可溝通的圖表。
4. [Geospatial Data in Python](geospatial-data-in-python.md)（選讀）: 資料帶有位置欄位時，geometry、CRS 與空間關係。
5. 追蹤群組隨時間的留存 / 流失：改用存活分析，見 [Kaplan–Meier](../statistics/survival-analysis/kaplan-meier.md)。

## 這一章要解決什麼

- 我拿到的新資料集，第一步該看什麼？
- 哪些欄位有資料品質風險，會影響後面分析？
- 如果資料有經緯度、區域邊界或地理圖層，分析前要先確認哪些前提？
- 缺失值到底要刪掉、填補，還是先保留並記錄？
- 圖表與摘要統計要如何搭配，避免只看平均數就下結論？

## 與其他章節的銜接

- 欄位整理與索引操作可搭配 [pandas](../python-foundations/pandas/README.md)。
- 視覺化探索已整合到本章的 [Visualization](visualization/README.md) 子章節。
- 當資料品質確認後，再進入 [Statistics](../statistics/README.md) 或 [Machine Learning](../machine-learning/README.md)。
