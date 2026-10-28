[Statistics](../README.md) › [存活分析](README.md) › Cox 模型

# Cox 比例風險模型 (Cox Proportional Hazards Model)

存活分析的主力模型：在 KM / log-rank 之上，可**同時納入多個共變數**，分配假設又很少。它是**半參數 (semi-parametric)** 模型：基線風險的形狀不做假設（無母數部分），共變數效果假設為乘法結構（參數部分）。生醫、社會科學、商業存活分析的預設模型。

$$
h(t \mid \mathbf{x}) = \underbrace{h_0(t)}_{\text{共同的時間型態}} \cdot \underbrace{\exp(\beta_1 x_1 + \cdots + \beta_p x_p)}_{\text{個人相對基線的縮放}}
$$

| 元素 | 意義 |
| --- | --- |
| h₀(t) 基線風險 (baseline hazard) | 所有共變數 = 0 時的風險；**不需估計、不指定形狀** |
| exp(βₖ) **風險比 (hazard ratio, HR)** | xₖ 增加 1 單位、其他共變數固定時，風險的倍數 |
| 比例風險假設 (proportional hazards, PH) | 任兩人的風險比**不隨時間改變**：$h(t \mid x_1)/h(t \mid x_2) = \exp(\beta^\top(x_1 - x_2))$ |

係數以**部分概似 (partial likelihood)** 估計，只用到事件發生時風險集內誰發生事件的排序資訊。

## 解讀 Hazard Ratio

| HR | 意義 |
| --- | --- |
| 1.0 | 無關聯 |
| 2.0 | 任一時點的瞬間風險為 2 倍 |
| 0.5 | 瞬間風險減半（保護因子） |
| 1.5 | 風險高 50% |

> **HR 不是相對風險 (RR)，也不是 odds ratio**。它是**瞬間事件速率**的比值，不是累積機率的比值。HR = 2 不代表「整體發生事件的機率是 2 倍」，而是「在某一時刻仍處於風險中的人，事件發生速率是 2 倍」。絕對效果請搭配存活曲線、中位數或 RMST 報告，見 [結果解讀](interpretation.md)。

## Python 範例

```python
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
from lifelines.datasets import load_rossi

rossi = load_rossi()
cph = CoxPHFitter().fit(rossi, duration_col="week", event_col="arrest",
                        formula="fin + age + race + wexp + mar + paro + prio")
cph.print_summary(decimals=3)
cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]]
cph.concordance_index_                       # C-index（模型的區辨力）

cph.plot(hazard_ratios=True)                 # 森林圖 (forest plot)
plt.axvline(1, ls="--", color="gray"); plt.show()

# 特定個人檔案的預測存活曲線
profiles = pd.DataFrame({"fin": [1, 0], "age": 25, "race": 1, "wexp": 0, "mar": 0, "paro": 1, "prio": 3},
                        index=["Aid", "No Aid"])
cph.predict_survival_function(profiles).plot(); plt.show()
cph.plot_partial_effects_on_outcome("prio", values=[0, 3, 8])   # 改變單一共變數的效果
```

| 共變數 | HR | p | 解讀（控制其他變數） |
| --- | --- | --- | --- |
| fin（經濟補助） | 0.685 | 0.044 | 有補助者再被捕風險低 31.5% |
| age | 0.944 | 0.009 | 年齡每多 1 歲，風險低 5.6% |
| prio（前科數） | 1.095 | 0.002 | 每多 1 次前科，風險高 9.5% |

R 版本：

```r
library(survival); library(survminer)
m <- coxph(Surv(time, status) ~ age + sex + ph.ecog, data = lung)
summary(m)        # coef = log HR、exp(coef) = HR、Concordance = C-index
cox.zph(m)        # 比例風險檢定
ggforest(m, data = lung)
```

## 共變數

| 類型 | 做法 |
| --- | --- |
| 類別 | 虛擬編碼，指定參考組：`formula="C(race, Treatment(reference=0)) + ..."` |
| 連續 | 假設與 log-hazard **線性**；用 **martingale 殘差** vs 共變數 + LOWESS 檢查，曲線 → log、平方項或樣條 |
| 時間相依 (time-dependent) | 共變數會隨時間改變（檢驗值、是否已開始治療）→ 長格式 (start, stop, event)，用 `CoxTimeVaryingFitter` |

```python
from lifelines import CoxTimeVaryingFitter

# 長格式：同一人可有多列，每列是一段共變數固定的區間
long = pd.DataFrame({"id": [1, 1, 2], "start": [0, 10, 0], "stop": [10, 25, 8],
                     "treated": [0, 1, 0], "event": [0, 1, 0]})
CoxTimeVaryingFitter().fit(long, id_col="id", start_col="start", stop_col="stop", event_col="event")
```

> **不朽時間偏誤 (immortal time bias)**：第 10 週才開始的治療，不能被算到第 0–10 週的區間。共變數只能套用到正確的時間區間，否則保護效果會被高估。見 [核心概念](core-concepts.md#常見錯誤)。

## 分層 Cox 模型 (Stratified Cox)

某個共變數違反 PH 時，可以**依它分層**：每層有自己的基線風險，但共享其他共變數的係數。

```python
cph_strat = CoxPHFitter().fit(rossi, duration_col="week", event_col="arrest",
                              formula="fin + age + wexp + mar + paro + prio", strata=["race"])
```

分層變數**不再有 HR**。只有在需要控制它的干擾、但不需要估計它的效果時才用。

## 延伸模型

| 延伸 | 用途 |
| --- | --- |
| **懲罰 Cox (Lasso / Ridge / Elastic Net)** | 高維共變數（基因表現、多基因風險分數）；`CoxPHFitter(penalizer=0.1, l1_ratio=1.0)`、R `glmnet(family = "cox")` |
| 多狀態模型 (multistate) | 狀態轉移（健康 → 疾病 → 死亡） |
| 競爭風險 (Fine-Gray) | 多種互斥事件，見 [競爭風險](core-concepts.md#競爭風險-competing-risks) |
| 脆弱模型 (frailty) | 群集資料或未觀察的異質性（Cox 的隨機效應版本，類似 [混合效應模型](../regression-analysis/mixed-effects-models.md)） |
| 機器學習存活模型 | Random survival forest、gradient boosting survival（`scikit-survival`） |

> 生資應用：從基因表現建立預後模型時，常見流程是單變數 Cox 篩選 → Lasso-Cox 選基因 → 計算風險分數 → 以中位數分高 / 低風險組畫 KM + log-rank。注意：在**同一份資料**上選基因又評估會嚴重高估表現，必須用獨立驗證世代或交叉驗證，見 [模型診斷](diagnostics.md#校準與驗證)。

下一步：檢查 PH 假設與其他診斷，見 [模型診斷](diagnostics.md)。
