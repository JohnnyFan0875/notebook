[Statistics](../README.md) › [存活分析](README.md) › 參數模型

# 參數存活模型 (Parametric Survival Models)

假設事件時間服從**特定分配**，明確定義風險函數的形狀。與 Cox（基線風險不指定）相比，能得到平滑的存活與風險估計、外推到觀察期之外、直接計算平均存活時間。

> 參數模型的力量來自結構；但分配選錯時，同樣的結構就變成負擔。Cox 通常是較安全的預設，當形狀假設**真的有資訊**時，參數模型才更強。

## Cox vs 參數模型

| | Cox | 參數模型 |
| --- | --- | --- |
| 基線風險 | 不指定（無母數） | 由已知分配明確建模 |
| 輸出 | 風險比 (HR) | 存活、風險、平均時間、時間比 |
| 外推 | 不行 | 可以（但要小心） |
| 適用 | 預後因子分析 | 外推、模擬、成本效益、可靠度、小樣本 |

## 常見分配

| 分配 | 風險形狀 | 參數 | 典型應用 |
| --- | --- | --- | --- |
| **Exponential** 指數 | 固定 | 1（λ） | 設備可靠度、簡單過程（無記憶性） |
| **Weibull** | 單調遞增或遞減 | 2（λ 尺度、k 形狀） | 醫學存活、可靠度測試；**最常用** |
| Gompertz | 指數遞增 | 2 | 人類死亡率 |
| **Log-normal** 對數常態 | 先升後降 | 2 | 生物恢復期、潛伏期 |
| **Log-logistic** | 先升後降、尾巴較厚 | 2 | 有晚期事件的長期存活；存活函數有封閉解 |

Weibull：$S(t) = \exp[-(t/\lambda)^k]$、$h(t) = \frac{k}{\lambda}(t/\lambda)^{k-1}$；k > 1 風險遞增、k < 1 遞減、k = 1 為指數分配。各函數的關係見 [存活與風險函數](survival-hazard-functions.md)。

| 風險看起來… | 候選分配 |
| --- | --- |
| 大致固定 | Exponential |
| 單調遞增或遞減 | Weibull |
| 先升後降 | Log-normal、Log-logistic |
| 厚尾、有晚期事件 | Log-logistic |

不要只因方便而選分配：把配適曲線疊在 KM 上，並比較候選模型的 AIC。

## 兩種參數化：PH 與 AFT

| 參數化 | 模型 | 係數解讀 | 適用分配 |
| --- | --- | --- | --- |
| 比例風險 (PH) | $h_i(t) = h_0(t; \theta)\, e^{\beta^\top x_i}$ | exp(β) = HR | Exponential、Weibull、Gompertz |
| **加速失敗時間 (accelerated failure time, AFT)** | $\log T_i = \mu + \beta^\top x_i + \sigma\varepsilon$ | exp(β) = **時間比 (time ratio)**；> 1 存活時間延長 | Weibull、Log-normal、Log-logistic |

Weibull 同時屬於 PH 與 AFT 兩族。PH 成立時，參數模型與 Cox 的 HR 會很接近；**PH 不成立時，AFT 是常見的替代方案**，見 [模型診斷](diagnostics.md#違反-ph-時的對策)。

## Python 範例

```python
import matplotlib.pyplot as plt
from lifelines import (KaplanMeierFitter, ExponentialFitter, WeibullFitter,
                       LogNormalFitter, LogLogisticFitter, WeibullAFTFitter)
from lifelines.datasets import load_rossi

rossi = load_rossi()
T, E = rossi["week"], rossi["arrest"]

# 1. 無共變數：比較候選分配
ax = KaplanMeierFitter().fit(T, E, label="KM").plot_survival_function(color="black")
for f in [ExponentialFitter(), WeibullFitter(), LogNormalFitter(), LogLogisticFitter()]:
    f.fit(T, E)
    f.plot_survival_function(ax=ax, ci_show=False)
    print(f"{f.__class__.__name__:20s} AIC = {f.AIC_:.1f}")      # 越小越好
plt.show()

# 2. 有共變數：Weibull AFT 迴歸
aft = WeibullAFTFitter().fit(rossi, duration_col="week", event_col="arrest", formula="fin + age + prio")
aft.print_summary()                          # exp(coef) = 時間比
aft.predict_median(rossi.head())             # 每個人的預測中位存活時間
```

R（`flexsurv`）：

```r
library(survival); library(flexsurv)
m <- flexsurvreg(Surv(time, status) ~ age + treatment, data = clinical_data, dist = "weibull")
summary(m); plot(m, type = "survival")
# 也可用 survreg(Surv(time, status) ~ x, dist = "weibull")（AFT 參數化）
```

## 評估

| 檢查 | 做法 |
| --- | --- |
| 配適度 | 候選模型的 AIC |
| 圖形 | 預測曲線 vs KM 曲線；Weibull 的 log(−log S) vs log t 應為直線 |
| 殘差 | Cox-Snell 殘差應近似 Exp(1)（其累積風險圖應沿 45° 線） |
| 與 Cox 比較 | PH 成立時結果應相近 |

## 何時參數模型勝過 Cox

- 需要**外推**到觀察期之外（長期追蹤、成本效益分析的終身模型）
- 樣本不大，而合理的形狀假設能穩定估計
- 需要以時間表達的摘要（平均存活、時間比）
- 模擬、衛生經濟學、可靠度工程需要完整的分配
- 有左設限或區間設限（概似框架可直接處理）

| 優點 | 限制 |
| --- | --- |
| 平滑連續的存活與風險估計 | 需要正確的分配假設 |
| 可外推 | 設定錯誤 → 結果有偏 |
| 直接估計平均 / 中位存活時間 | 彈性不如 KM |
| 適合模擬與經濟模型 | 可能配適不了複雜的風險型態（考慮 flexible parametric / spline 模型） |

> 在觀察期內配適得好，**不保證**外推可靠。長期預測的可信度，完全取決於背後的分配假設。
