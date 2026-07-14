# Model Interpretability

Interpretability 是在回答「模型到底根據什麼在做判斷」。它可以幫你建立信任、協助除錯，也能讓利害關係人知道模型抓到的是合理訊號還是可疑代理變數。

## 先分兩類問題

### 全域解釋

模型整體最依賴哪些特徵？哪些方向的變化通常會影響預測？

### 區域解釋

為什麼某一筆樣本被預測成這個結果？

## Common Approaches

- **Coefficients**: useful for linear and [logistic regression](../supervised-learning/classification/logistic-regression.md), but interpretation depends on scaling, collinearity, and feature coding.
- **Feature importance**: common for tree-based models, but importance can be unstable or biased toward high-cardinality features.
- **Permutation importance**: model-agnostic and often a better default than impurity-based importance.
- **Partial dependence / ICE**: show how predictions change as a feature changes.
- **SHAP**: local and global explanations for complex models.

## Important Cautions

- correlated features can distort importances
- a feature being important does not mean it is causal
- explanations of a single prediction do not automatically summarize the whole model

## 怎麼選工具

| 情境 | 優先方法 | 原因 |
| --- | --- | --- |
| 線性或邏輯斯模型 | coefficient + domain review | 直接、可對照假設 |
| 樹模型想看整體重要度 | permutation importance | 比 impurity-based importance 更穩健 |
| 想看特徵如何改變預測 | PDP / ICE | 可視化效果方向與非線性 |
| 想解釋單筆預測 | SHAP / local explanation | 適合 case review |

## Practical Advice

- start with simple model behavior checks
- use permutation importance for a more robust first pass
- pair explanations with slice-based evaluation and domain knowledge
- if the explanation conflicts with domain knowledge, investigate data leakage or proxy variables first

## Related Concepts

- [Model Diagnostics](model-diagnostics.md)
- [Feature Selection](../preprocessing/feature-selection.md)
- [Random Forest](../supervised-learning/ensemble/random-forest.md)
- [Statsmodels Documentation](../packages/statsmodels/README.md)

[Back to Interpretability and Diagnostics](README.md)
