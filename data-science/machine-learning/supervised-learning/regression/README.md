[Machine Learning](../../README.md) › [監督式學習](../README.md) › 迴歸

# 迴歸 (Regression)

預測連續數值：價格、需求量、存活時間以外的連續結果、藥物反應 (IC50)、基因表現量。

## 建議順序

```
線性迴歸（baseline）→ Ridge / Lasso / Elastic Net（特徵多、共線）→ 迴歸樹（非線性）→ 集成方法
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [線性迴歸](linear.md) | 最小平方法、係數解讀、ML vs 統計用法 | 最簡單的 baseline 怎麼做？ |
| [Ridge](ridge.md) | L2 正則化、共線性 | 特徵相關時怎麼穩定係數？ |
| [Lasso](lasso.md) | L1 正則化、自動特徵選擇 | 怎麼讓不重要的係數變 0？ |
| [Elastic Net](elastic-net.md) | L1 + L2、相關特徵群 | 特徵多又高度相關時怎麼辦？ |
| [迴歸樹](decision-tree.md) | 分段常數預測、深度控制 | 非線性關係怎麼抓？ |

三種正則化的係數路徑比較見 [正則化](../../foundations/regularization.md)。

## 提醒

| 提醒 | 說明 |
| --- | --- |
| 不只看 R² | 看誤差尺度（RMSE、MAE）與殘差型態，見 [迴歸指標](../../evaluation/mse-rmse.md) |
| 目標高度右偏 | 考慮 log 轉換或 Poisson / Gamma 損失 |
| 目標是計數 | 用 [Poisson / 負二項 GLM](../../../statistics/regression-analysis/glm-count-models.md) 或 `HistGradientBoostingRegressor(loss="poisson")` |
| 目標是存活時間（有設限） | 不能直接迴歸，見 [存活分析](../../../statistics/survival-analysis/README.md) |
