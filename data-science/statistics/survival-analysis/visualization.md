[Statistics](../README.md) › [存活分析](README.md) › 視覺化

# 存活分析視覺化 (Visualization)

視覺化不是裝飾：KM 曲線是所有存活分析的起點、log-log 圖是 PH 假設的視覺檢查、森林圖是 Cox 結果的標準呈現。每種圖都有特定的診斷或溝通目的。從 DataFrame 快速作圖見 [Pandas: Visualization](../../data-manipulation-and-eda/visualization/pandas-plotting.md)。

## 圖表總覽

| 圖 | 目的 | 怎麼讀 | 詳見 |
| --- | --- | --- | --- |
| **Kaplan-Meier 曲線** | 各組隨時間的存活機率 | 事件 → 往下跳；設限 → 刻度標記；陰影為 CI | [Kaplan-Meier](kaplan-meier.md) |
| **風險表** (at-risk table) | 各時點仍在追蹤中的人數 | 人數少的區段估計不穩 | [Kaplan-Meier](kaplan-meier.md) |
| 累積風險圖 (Nelson-Aalen) | 累積風險隨時間 | 指數分配下為直線；各組大致成比例 → PH 合理 | [存活與風險函數](survival-hazard-functions.md) |
| log-log 圖 | 檢查 PH 假設 | 平行 → PH 成立；交叉 → 違反 | [模型診斷](diagnostics.md) |
| **森林圖** (forest plot) | Cox 模型各共變數的 HR 與 95% CI | 方塊 = HR、橫線 = CI、HR = 1 的垂直線 = 無效果 | [Cox 模型](cox-ph-model.md) |
| 調整後存活曲線 | 控制共變數後，各組的預測存活 | 比原始 KM 更能反映調整後的差異 | [Cox 模型](cox-ph-model.md) |
| Schoenfeld 殘差圖 | 係數是否隨時間改變 | LOWESS 水平 → PH 成立 | [模型診斷](diagnostics.md) |
| Martingale 殘差圖 | 連續共變數的函數形式 | 非水平 → 考慮轉換或樣條 | [模型診斷](diagnostics.md) |
| Deviance 殘差圖 | 離群個體 | \|值\| > 2 值得檢查 | [模型診斷](diagnostics.md) |
| 校準圖 | 預測 vs 觀察存活 | 貼近 45° 線 = 校準良好 | [模型診斷](diagnostics.md#校準與驗證) |
| 累積發生曲線 (CIF) | 競爭風險下各事件的累積發生率 | 取代 1 − KM | [核心概念](core-concepts.md#競爭風險-competing-risks) |
| Heatmap | 依分層 / 風險分數 / 基因表現群的存活機率 | 多世代、omics 分析常用 | — |

Nelson-Aalen 累積風險估計：$\hat H(t) = \sum_{t_i \le t} d_i / n_i$。

## Python

```python
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, NelsonAalenFitter, CoxPHFitter
from lifelines.plotting import add_at_risk_counts
from lifelines.statistics import logrank_test, proportional_hazard_test

# KM + CI + 風險表 + log-rank p（df 含 time、status、group）
fig, ax = plt.subplots(figsize=(8, 5))
fits = []
for g, sub in df.groupby("group"):
    k = KaplanMeierFitter().fit(sub["time"], sub["status"], label=str(g))
    k.plot_survival_function(ax=ax, ci_show=True, show_censors=True)
    fits.append(k)
add_at_risk_counts(*fits, ax=ax)
a, b = [sub for _, sub in df.groupby("group")]
p = logrank_test(a["time"], b["time"], a["status"], b["status"]).p_value
ax.set(title=f"log-rank p = {p:.3f}", xlabel="Time (months)", ylabel="Survival probability")
plt.tight_layout(); plt.show()

# 累積風險
NelsonAalenFitter().fit(df["time"], df["status"]).plot(); plt.show()

# 森林圖 + PH 檢定
cph = CoxPHFitter().fit(df, duration_col="time", event_col="status")
cph.plot(hazard_ratios=True); plt.show()
proportional_hazard_test(cph, df, time_transform="rank").print_summary()
```

## R（survminer）

```r
library(survival); library(survminer)
fit <- survfit(Surv(time, status) ~ treatment, data = clinical_data)

ggsurvplot(fit, data = clinical_data, pval = TRUE, conf.int = TRUE, risk.table = TRUE,
           surv.median.line = "hv", xlab = "Time (months)", ggtheme = theme_minimal())
ggsurvplot(fit, fun = "cumhaz", data = clinical_data)       # 累積風險
ggforest(cox_model, data = clinical_data)                     # 森林圖
plot(cox.zph(cox_model))                                      # Schoenfeld 殘差
# 校準：rms::calibrate()
```

## 發表級圖表建議

| 元素 | 建議 |
| --- | --- |
| 顏色 | 跨圖一致（如處理 A = 藍、B = 紅）；考慮色盲友善配色 |
| 座標軸 | 標示時間單位（月、年）；y 軸從 0 到 1 |
| 信賴區間 | 適當時以半透明陰影呈現 |
| 圖例 | 清楚標示組別與樣本數 |
| 標註 | 中位存活時間、log-rank p 值、HR（95% CI） |
| 風險表 | **放在 KM 圖下方** |
| 時間範圍 | 截在風險集仍合理的時間點，避免過度強調不穩定的尾端 |

> 只能放幾張圖時，優先順序：(1) KM 曲線 + CI；(2) 風險表；(3) 有配適 Cox 時的 HR 森林圖。沒有風險表的極簡存活圖，通常比稍微擁擠但有正確脈絡的圖資訊更少。
