[Machine Learning](../README.md) › [模型評估](README.md) › 指標的不確定性

# 評估指標的不確定性 (Uncertainty in Evaluation Metrics)

測試集分數也是從有限樣本估計出來的統計量。測試集只有幾十到幾百筆時（生醫研究的常態），「AUC 0.85 vs 0.83」幾乎一定只是雜訊。報告效能時要附上**信賴區間**，比較模型時要用**配對**的方法。

## 測試集有多小算小

Accuracy 的 95% 信賴區間（Wilson），真實 accuracy 約 0.8 時：

| 測試樣本數 | 95% CI 大約 |
| --- | --- |
| 30 | 0.63 – 0.91 |
| 100 | ±0.08 |
| 1,000 | ±0.025 |

AUC、recall 等指標的有效樣本數是**陽性的個數**：100 筆測試資料中只有 10 個陽性時，recall 只能是 0.1 的倍數。

## 單一模型：信賴區間

```python
import numpy as np
from scipy.stats import bootstrap
from sklearn.metrics import roc_auc_score
from statsmodels.stats.proportion import proportion_confint

# 承乳癌範例：測試集 171 筆，邏輯斯迴歸
# 1. Accuracy / recall 這類比例：二項信賴區間
k, n = 166, 171                                       # 答對 166 筆
proportion_confint(k, n, method="wilson")             # (0.933, 0.987)

# 2. AUC 這類沒有簡單公式的指標：bootstrap（對 y 與分數成對重抽樣）
res = bootstrap((y_test, y_prob), roc_auc_score, paired=True, vectorized=False,
                n_resamples=2000, method="percentile", random_state=0)
res.confidence_interval                                # AUC 0.9975, CI (0.992, 1.000)
```

Bootstrap 原理見 [Bootstrap](../../statistics/probability-and-distributions/monte-carlo-simulation.md#拔靴法-bootstrap)。

## 比較兩個模型：要配對

兩個模型在**同一個測試集**上評估，誤差高度相關，不能各自算 CI 再看是否重疊。

| 比較對象 | 方法 |
| --- | --- |
| AUC 或任意指標 | 配對 bootstrap：每次重抽樣同時算兩個模型的指標差，看差值的 CI 是否包含 0 |
| AUC（常態近似） | DeLong 檢定（R `pROC::roc.test`；sklearn 沒有內建） |
| Accuracy（同一閾值下的對錯） | McNemar 檢定：只看兩模型**意見不同**的樣本 |
| 多個模型 × 多個資料集 | Friedman + Nemenyi 事後檢定 |

```python
from statsmodels.stats.contingency_tables import mcnemar

# 1. 配對 bootstrap：AUC 差值
diff = lambda yt, a, b: roc_auc_score(yt, a) - roc_auc_score(yt, b)
res = bootstrap((y_test, p_lr, p_nb), diff, paired=True, vectorized=False,
                n_resamples=2000, method="percentile", random_state=0)
res.confidence_interval            # 差 0.0015，CI (−0.003, 0.007) → 包含 0

# 2. McNemar：2×2 表 = [[兩者皆對, 只有 A 對], [只有 B 對, 兩者皆錯]]
a = (pred_lr == y_test); b = (pred_nb == y_test)
table = [[(a & b).sum(), (a & ~b).sum()], [(~a & b).sum(), (~a & ~b).sum()]]   # [[158, 8], [2, 3]]
mcnemar(table, exact=True).pvalue  # 0.11
```

乳癌範例中，邏輯斯迴歸 accuracy 0.971、Naive Bayes 0.936，看起來差了 3.5 個百分點；但兩者意見不同的樣本只有 10 個（8 vs 2），McNemar p = 0.11，在 171 筆測試資料上**無法確定誰比較好**。

## 交叉驗證分數的不確定性

| 注意 | 說明 |
| --- | --- |
| CV 各 fold 的 SD 不是嚴格的標準誤 | 各 fold 的訓練資料大幅重疊，不獨立；SD 會低估真正的不確定性 |
| 用同一組 folds 比較模型 | 看每個 fold 的分數差，而不是兩個平均數 |
| 重複 CV | `RepeatedStratifiedKFold` 讓估計更穩定，但不會讓樣本變多 |
| 差距小於 fold 間 SD | 選較簡單的模型 |

> 只報「AUC = 0.87」不夠；寫成「AUC 0.87（95% CI 0.81–0.92，n = 150，陽性 40）」，讀者才能判斷可信度。調參時看到的最佳分數還帶有挑選偏誤，見 [Nested CV](../workflow/cross-validation.md#nested-cv)。
