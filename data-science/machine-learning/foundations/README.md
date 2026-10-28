[Machine Learning](../README.md) › 基礎概念

# 基礎概念 (Foundations)

幾乎每個建模決策背後都是這些觀念：模型要在**沒看過的資料**上表現好，而不是在訓練資料上。

## 建議順序

```
問題類型 → 泛化 → 損失函數 → Bias-Variance → 過擬合 / 欠擬合 → 正則化
                                      ↓
         資料洩漏 → 高維小樣本 → 抽樣與代表性 → 評估思維 → 特徵工程 → Basetable
```

前半段是「模型為什麼會失敗」，後半段是「資料與驗證設計為什麼會讓你以為它沒失敗」。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [問題類型與學習範式](problem-types-and-learning-paradigms.md) | 監督 / 非監督 / 自監督、迴歸 / 分類 / 排序 | 這是哪一類問題？ |
| [泛化](generalization.md) | 訓練 / 驗證 / 測試誤差、分布偏移 | 為什麼訓練分數高不代表模型好？ |
| [損失函數](loss-functions.md) | MSE、MAE、Huber、log loss、hinge；與 MLE 的對應 | 模型實際在最佳化什麼？ |
| [Bias-Variance 權衡](bias-variance-tradeoff.md) | 誤差分解、模型複雜度 | 誤差從哪裡來？ |
| [過擬合與欠擬合](overfitting-underfitting.md) | 症狀、學習曲線、對策 | 模型太複雜還是太簡單？ |
| [正則化](regularization.md) | L1 / L2 / Elastic Net、其他限制複雜度的方法 | 怎麼控制模型複雜度？ |
| [資料洩漏](data-leakage.md) | 洩漏型態、預防做法、檢查清單 | 分數是不是作弊來的？ |
| [高維小樣本](high-dimensional-data.md) | p ≫ n、維度詛咒、nested CV、生資情境 | 基因數遠多於樣本數時怎麼建模？ |
| [抽樣與代表性](sampling-and-representativeness.md) | 抽樣 / 選擇偏誤、分布偏移、問卷 | 訓練資料能代表上線後的資料嗎？ |
| [特徵工程原則](feature-engineering-principles.md) | 資料理解、刪除、轉換、缺失、時間 | 什麼是好特徵？ |
| [Basetable 與時間感知特徵](basetable-and-time-aware-feature-engineering.md) | reference date、時間窗、多快照、predictor insight | 事件資料怎麼整理成一張安全的建模表？ |
