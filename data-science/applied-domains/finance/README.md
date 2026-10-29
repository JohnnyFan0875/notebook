[Data Science](../../README.md) › [應用領域](../README.md) › Finance

# 金融 (Finance)

用金融資料作為統計、時間序列與分類模型的應用場景。金融資料高度雜訊、非平穩，不同頻率下的結論可能完全不同；很多方法（折現、共變異矩陣、尾部風險、回測紀律、校準與門檻、存活機率加權）都能遷移到其他領域。

## 建議順序

```
金融概念與資料清理 → 投資組合與風險 → 交易策略與回測
                  ↘ 信用風險模型（分類 → 決策）   保險年金（存活機率 × 折現）
```

| 筆記 | 內容 | 可遷移的方法 |
| --- | --- | --- |
| [金融基本概念](financial-concepts.md) | 貨幣時間價值、折現、NPV / IRR、債券、duration / convexity、金融資料清理 | 現金流折現、敏感度（一階 / 二階近似）、時間索引紀律 |
| [投資組合與風險](portfolio-and-risk.md) | 報酬與波動、分散、Sharpe、因子模型、效率前緣、VaR / CVaR、EVT、股價模擬 | 共變異矩陣與收縮估計、蒙地卡羅、厚尾分布、滾動估計 |
| [交易策略與回測](trading-strategies-and-backtesting.md) | 技術指標、訊號 → 部位、基準、績效指標、過擬合 | 回測紀律、look-ahead bias、walk-forward 驗證、多重比較 |
| [信用風險模型](credit-risk-modeling.md) | PD / EAD / LGD、logistic 與 boosting、校準、核貸門檻 | 分類模型評估、校準、成本不對稱下的門檻 |
| [保險與年金估值](insurance-and-annuity-valuation.md) | 壽命表、EPV、年金、壽險 | 存活機率加權的現金流 |

金融報酬率的自相關（動能、均值回歸、波動聚集）見 [時間序列：自相關](../../statistics/time-series-analysis/autocorrelation.md#金融情境動能與均值回歸)。

## 閱讀提醒

| 提醒 | 理由 |
| --- | --- |
| 價格序列與報酬率序列的性質不同 | 價格非平穩，報酬率接近平穩；不要混著判讀 |
| 統計顯著不等於可交易 | 還要考慮交易成本、容量與穩定性 |
| 先和 buy-and-hold 比 | 最簡單的基準常已經很難打敗 |
| 把時間點與狀態機率分開建模 | 現金流受存活、死亡或違約影響時 |
