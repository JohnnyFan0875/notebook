[Data Science](../README.md) › 資料處理與 EDA

# 資料處理與探索式分析 (Data Manipulation & EDA)

建模之前先把資料看懂。很多分析失敗不是模型選錯，而是太早建模，沒先確認欄位定義、缺失、重複、離群值與分布。

```text
Profiling → 缺失機制 → 單變數 / 雙變數圖 → 記錄要修的欄位 → 統計 / 建模
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [EDA 流程](eda-workflow.md) | profiling 檢查表、起手式程式碼、omics 矩陣的 QC、判讀訊號 | 拿到新資料第一步看什麼？ |
| [缺失機制](missing-data.md) | MCAR / MAR / MNAR、刪除策略、生資常見的缺失型態 | 缺值能直接刪嗎？會造成什麼偏誤？ |
| [視覺化](visualization/README.md) | 圖表設計原則、Matplotlib、Seaborn、pandas plotting、ggplot2 | 什麼問題配什麼圖？怎麼畫才不誤導？ |
| [地理空間資料](geospatial-data-in-python.md)（選讀） | GeoPandas、geometry、CRS、空間 join | 資料有經緯度時要注意什麼？ |

| 相關 | 連結 |
| --- | --- |
| 資料品質對統計的影響、生資陷阱 | [Statistics：資料品質](../statistics/descriptive-statistics/data-quality.md) |
| 多變數 EDA、相關矩陣、Simpson's paradox | [多變量探索](../statistics/multivariate-analysis/multivariate-eda.md) |
| 工具：缺值 API | [pandas 缺值](../python-foundations/pandas/missing-data.md)、[R naniar](../r-foundations/missing-data.md) |
| 插補、離群值處理 | [Imputation](../machine-learning/preprocessing/imputation.md)、[Outlier Handling](../machine-learning/preprocessing/outlier-handling.md) |
| 群組隨時間的留存 / 流失 | [Kaplan–Meier](../statistics/survival-analysis/kaplan-meier.md) |
