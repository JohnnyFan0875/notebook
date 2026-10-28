[Statistics](../README.md) › [存活分析](README.md) › Log-rank 檢定

# Log-rank 檢定 (Log-Rank Test)

比較兩組以上存活曲線的標準無母數檢定，正確處理設限。它是 KM 曲線的配套檢定，地位就像 t 檢定之於平均數：兩條 KM 曲線看起來不同，不代表統計上顯著不同。

$$
H_0: S_1(t) = S_2(t)\ \text{對所有 } t \quad (\text{等價於各組 hazard 相同})
$$

## 原理

1. 在每個事件時間 tⱼ，若 H₀ 為真，各組的**期望事件數**依其在風險集中的比例分配
2. 加總所有時間點的（觀察 − 期望）
3. 標準化後在 H₀ 下服從 χ²，df = 組數 − 1

$$
\chi^2 = \frac{\left(\sum_j (O_{1j} - E_{1j})\right)^2}{\text{Var}}
$$

標準 log-rank 對所有事件時間給**相同權重**，在 hazard ratio 大致固定（比例風險）時檢定力最高。

## Python 範例

```python
import pandas as pd
from itertools import combinations
from lifelines.datasets import load_rossi
from lifelines.statistics import logrank_test, multivariate_logrank_test, pairwise_logrank_test

rossi = load_rossi()
T, E = rossi["week"], rossi["arrest"]
aid = rossi["fin"] == 1

# 兩組
res = logrank_test(T[aid], T[~aid], event_observed_A=E[aid], event_observed_B=E[~aid])
res.test_statistic, res.p_value

# 加權版本（事先決定！）
logrank_test(T[aid], T[~aid], E[aid], E[~aid], weightings="wilcoxon")      # Gehan-Breslow
logrank_test(T[aid], T[~aid], E[aid], E[~aid], weightings="tarone-ware")

# 三組以上
rossi["prio_group"] = pd.cut(rossi["prio"], bins=[-1, 0, 3, 20], labels=["None", "1-3", "4+"])
multivariate_logrank_test(T, rossi["prio_group"], E).p_value

# 事後兩兩比較：記得校正 p 值
pw = pairwise_logrank_test(T, rossi["prio_group"], E)
pw.summary                  # 對 p 值再做 Holm / Bonferroni，見多重檢定校正
```

R：`survdiff(Surv(time, status) ~ sex, data = lung)`。

> 多組 log-rank 顯著只代表「至少一組不同」，要找出哪幾組需做兩兩比較並 [校正多重檢定](../inferential-statistics/multiple-testing.md)。

## 加權變體

| 變體 | tⱼ 的權重 | 最敏感於 | lifelines |
| --- | --- | --- | --- |
| 標準 log-rank | 1 | 比例風險、**晚期**差異 | 預設 |
| Gehan-Breslow (Wilcoxon) | nⱼ（風險集大小） | **早期**差異 | `"wilcoxon"` |
| Tarone-Ware | √nⱼ | 早晚平衡 | `"tarone-ware"` |
| Peto-Peto | Ŝ(tⱼ) | 對晚期設限較穩健 | `"peto"` |
| Fleming-Harrington (p, q) | Ŝ^p (1−Ŝ)^q | 可自訂 | `"fleming-harrington"` |

預期效果出現在早期（例如疫苗在前幾週預防感染）→ Gehan-Breslow；預期長期效果 → 標準 log-rank。**看資料之前就要指定**，事後挑 p 值最小的權重就是 p-hacking。

## 限制

| 限制 | 說明 | 替代 |
| --- | --- | --- |
| 無法調整共變數 | 只比較組別，無法控制干擾因子 | [Cox 模型](cox-ph-model.md) |
| 曲線**交叉**時檢定力大減 | 一組早期較好、另一組晚期較好，正負抵消 | RMST 差異、加權 log-rank |
| 最適合比例風險 | hazard ratio 固定時最有力 | Cox + PH 檢查、分層 Cox |
| 只檢定「是否不同」 | 不告訴你差多少 | Cox 的 hazard ratio、中位數差、RMST 差 |
| 對大量晚期設限敏感 | — | 限制分析時間範圍、RMST |

> Log-rank 只回答「這些組不同嗎？」，不回答「差多少？」或「為什麼？」。要量化效果並調整共變數，進入 [Cox 模型](cox-ph-model.md)。曲線交叉時，把圖放在顯眼處並考慮 RMST 或加權方法。
