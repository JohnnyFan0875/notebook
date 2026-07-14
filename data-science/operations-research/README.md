# Operations Research

這個模組整理的是資料科學裡比較偏 prescriptive 的那一側，也就是當問題不只是「會發生什麼」，而是「在約束下應該怎麼做」時，常見的建模語言與決策框架。

Key point: operations research 的核心不是把數學寫得很複雜，而是把決策變數、目標與約束翻成一個可以被系統性求解的模型。

## Topics

- [Optimization in Python](optimization-in-python.md)
- [Supply Chain Optimization](supply-chain-optimization.md)

## 這個模組回答什麼問題

- 在容量、需求、成本與邏輯限制之下，最佳決策是什麼？
- 哪些約束是真正卡住系統的 bottleneck？
- 若需求或成本改變，最佳解會不會一起改變？

## 建議閱讀順序

1. 先看 [Data Communication](../data-communication/README.md)，先把 business question 和 analytical question 分清楚。
2. 再看 [Statistics](../statistics/README.md)，建立不確定性與輸入資料品質的基本感覺。
3. 再看 [Optimization in Python](optimization-in-python.md)，建立 objective、constraints 與 solver 的基本直覺。
4. 再看 [Supply Chain Optimization](supply-chain-optimization.md)，把 prescriptive model 的骨架與限制條件直覺建立起來。

## 與其他章節的關係

- [Statistics](../statistics/README.md): 幫你判斷需求、成本、處理時間與其他輸入是否可信。
- [Machine Learning](../machine-learning/README.md): ML 常回答「會發生什麼」，OR 則接著回答「應該怎麼做」。
- [Process Analytics](../process-analytics/README.md): 若 bottleneck 已被找出，OR 常負責後續的資源配置與改善方案。

## 實務提醒

- solver 找到的最優解，只對你給進去的目標、限制與假設成立。
- 若輸入資料很不穩定，先做 sensitivity analysis，比直接追求唯一最佳解更重要。
- OR 最有價值的地方通常不是數學炫技，而是把 trade-off 說清楚。
