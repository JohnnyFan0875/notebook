[Statistics](../README.md) › [存活分析](README.md) › 模型診斷

# Cox 模型診斷 (Model Diagnostics & Violations)

配適 Cox 模型不是最後一步。忽略假設檢查就發表 Cox 結果，等同於發表線性迴歸卻不看殘差圖。一般迴歸的診斷（槓桿、Cook's distance）見 [多變量：模型診斷](../multivariate-analysis/assumptions-diagnostics.md) 與 [Statsmodels: Diagnostics](../../machine-learning/packages/statsmodels/diagnostics.md)。

**檢查順序**：(1) 比例風險 → (2) 連續共變數的函數形式 → (3) 影響點 → (4) 區辨力 → (5) 校準。不要直接跳到 C-index：模型可能排序得很好，但結構上設定錯誤。

| 檢查 | 工具 | 合格 |
| --- | --- | --- |
| 比例風險 (PH) | log-log 圖、Schoenfeld 殘差 | 平行；無時間趨勢、p > 0.05 |
| 函數形式 | Martingale 殘差 vs 共變數 | LOWESS 接近水平 |
| 影響點 | dfbeta 殘差 | 無極端值 |
| 配適不佳的個體 | Deviance 殘差 | \|值\| < 2 |
| 區辨力 | C-index | > 0.7 為佳 |
| 校準 | 預測 vs 觀察存活 | 貼近 45° 線 |

## 比例風險假設 (PH)

違反時：估計的 HR 是跨時間的**平均**，可能不代表任何特定時期；CI 可能太窄；實質結論可能完全錯誤。

### 視覺檢查：log-log 圖

在 PH 下，$\log(-\log \hat S(t)) = \log H_0(t) + \beta^\top x$，各組曲線對 log t 應該**平行**（垂直距離固定 = log HR 固定）。交叉或系統性分開 → 違反 PH。

### 正式檢定：Schoenfeld 殘差

每個共變數在每個事件時間都有一個 Schoenfeld 殘差。PH 成立時，殘差應**沒有時間趨勢**。H₀：βₖ(t) 不隨時間改變。

```python
import numpy as np
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.datasets import load_rossi

rossi = load_rossi()
T, E = rossi["week"], rossi["arrest"]
cph = CoxPHFitter().fit(rossi, duration_col="week", event_col="arrest",
                        formula="fin + age + race + wexp + mar + paro + prio")

# 1. 一行完成 Schoenfeld 檢定 + 殘差圖 + 修正建議（首選）
cph.check_assumptions(rossi, p_value_threshold=0.05, show_plots=True)

# 2. log-log 圖
for g, label in [(1, "Aid"), (0, "No Aid")]:
    m = rossi["fin"] == g
    sf = KaplanMeierFitter().fit(T[m], E[m]).survival_function_.iloc[:, 0]
    sf = sf[(sf > 0) & (sf < 1)]
    plt.plot(np.log(sf.index), np.log(-np.log(sf)), label=label)
plt.xlabel("log(t)"); plt.ylabel("log(-log S(t))"); plt.legend(); plt.show()

# 3. 其他殘差
mart = cph.compute_residuals(rossi, kind="martingale")       # 函數形式
dfb  = cph.compute_residuals(rossi, kind="delta_beta")       # 每個係數的影響點
dev  = cph.compute_residuals(rossi, kind="deviance")         # 配適不佳者，|dev| > 2
```

R：`cox.zph(m)` 與 `plot(cox.zph(m))`；`residuals(m, type = "dfbeta")`、`type = "deviance"`。

## 違反 PH 時的對策

| 情況 | 建議 |
| --- | --- |
| 單一共變數違反 | 依該變數**分層**（`strata=[...]`），見 [Cox 模型](cox-ph-model.md#分層-cox-模型-stratified-cox) |
| 效果隨時間改變且想估計 | 共變數 × 時間 交互作用（時間相依係數） |
| 整體都違反 | **加速失敗時間 (AFT)** 模型，見 [參數模型](parametric-models.md) |
| 風險曲線交叉 | 比較 RMST 而非 HR |
| 效果只在特定時段 | 分段指數模型 (piecewise exponential)、分段 HR |

```python
from lifelines import WeibullAFTFitter, CoxTimeVaryingFitter
from lifelines.utils import to_episodic_format

# 時間相依係數：轉成區間格式後加入 共變數 × 時間
long = to_episodic_format(rossi, duration_col="week", event_col="arrest")
long["prio_x_logt"] = long["prio"] * np.log(long["stop"])
CoxTimeVaryingFitter().fit(long, id_col="id", start_col="start", stop_col="stop",
                           event_col="arrest", formula="fin + age + prio + prio_x_logt")

# AFT：不假設比例風險
WeibullAFTFitter().fit(rossi, duration_col="week", event_col="arrest",
                       formula="fin + age + prio").print_summary()
```

**AFT 係數**：exp(β) 為**時間比 (time ratio / acceleration factor)**；> 1 → 事件發生較晚（存活時間延長）、< 1 → 較早。在工程可靠度或商業情境中，「存活時間的倍數」通常比 HR 更直覺。

## 區辨力：C-index

Concordance index：隨機取兩人，模型預測風險較高者確實較早發生事件的機率，是存活版的 [AUC](../../machine-learning/evaluation/roc-auc.md)。

| C-index | 解讀 |
| --- | --- |
| 0.5 | 隨機 |
| 0.6–0.7 | 普通 |
| 0.7–0.8 | 良好 |
| > 0.8 | 很好 |

```python
from lifelines.utils import concordance_index
concordance_index(rossi["week"], -cph.predict_partial_hazard(rossi), rossi["arrest"])   # 風險取負號
cph.concordance_index_                                                                 # 模型摘要內建
```

## 校準與驗證

| 類型 | 說明 | 工具 |
| --- | --- | --- |
| 內部驗證 | Bootstrap / 交叉驗證評估可重現性與樂觀偏誤 | R `rms::validate()`；Python `lifelines.utils.k_fold_cross_validation` |
| **外部驗證** | 套用到獨立世代 | 新資料上的 C-index、校準、時間相依 AUC |
| 校準圖 | 某時點預測存活 vs 觀察存活 | R `rms::calibrate()`；`lifelines.calibration.survival_probability_calibration` |
| 整體預測誤差 | 同時考量區辨與校準 | Brier score / integrated Brier score（`scikit-survival`） |

> C-index 高**不保證**校準：模型可能排序正確，但系統性高估或低估絕對存活機率。區辨力與校準是兩件獨立的事，都要檢查。
