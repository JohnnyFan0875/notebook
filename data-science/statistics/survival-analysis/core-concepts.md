[Statistics](../README.md) › [存活分析](README.md) › 核心概念與設限

# 核心概念與設限 (Core Concepts & Censoring)

最常見的錯誤：把存活資料當一般二元結果分析，完全忽略時間與設限，結果不只不準，連方向都可能錯。實驗設計的名詞（因子、實驗單位、干擾）見 [實驗設計核心概念](../experimental-design/core-concepts.md)。

## 兩個核心變數：(T, δ)

| 變數 | 說明 | 例子 |
| --- | --- | --- |
| 時間 T (time / duration) | 從**起點**到事件或設限的時間 | 診斷後 14.5 個月 |
| 事件 δ (event indicator) | 1 = 觀察到事件、0 = 設限 | 1 = 死亡、0 = 研究結束時仍存活 |

「存活」只是歷史名稱，事件可以是任何定義清楚、不重複的事件：流失、故障、違約、轉換、復發。

**起點 (time origin)** 必須明確且對所有人一致：診斷日、手術日、隨機分派日、治療開始日。

## 設限 (Censoring)

只知道存活時間的**一部分**：知道受試者**至少**活到某時間，但不知道事件何時（或是否）發生。

> 設限**不是缺失資料**，而是**部分資訊**。刪除設限觀測會丟掉真實資訊，並讓估計偏向較短的存活時間。

| 類型 | 說明 | 例子 |
| --- | --- | --- |
| **右設限** (right) | 觀察結束時事件尚未發生（**最常見**） | 研究結束時病人仍存活 |
| 行政設限 (administrative) | 研究在固定日期結束 | 所有人在資料截止日設限 |
| 失去追蹤 (loss to follow-up) | 受試者退出、搬家、失聯 | 病人不再回診 |
| Type I 設限 | 研究到預定時間停止 | 5 年試驗結束時存活者設限 |
| Type II 設限 | 研究到預定事件數停止 | 10 台機器測到 5 台故障為止 |
| 左設限 (left) | 事件在觀察開始前就已發生，確切時間不明 | 第一次抽血時已感染 |
| 區間設限 (interval) | 事件發生在兩個已知時間點之間 | 例行掃描時發現腫瘤復發 |

```
受試者 1: |────────● 事件 (t = 10)
受試者 2: |──────────────────○ 設限，研究結束 (t = 20)
受試者 3: |─────────────○ 失去追蹤 (t = 14)
受試者 4: |────● 事件 (t = 5)
時間:     0        10        20
```

> **非資訊性設限 (non-informative censoring)** 假設：設限的原因與事件風險無關。若高風險者更容易退出研究（例如病重轉院），估計會有偏誤。

KM 與 Cox 原生處理右設限；左設限與區間設限需要專門方法（Turnbull 估計量、以概似為基礎的 [參數模型](parametric-models.md)）。

## Python 資料結構

`lifelines` 需要整潔格式：每位受試者一列，至少有時間與事件欄。

```python
import numpy as np
import pandas as pd

data = pd.DataFrame({
    "time":      [10, 20, 14, 5, 26, 8, 18, 3],
    "event":     [1,  0,  0,  1, 0,  1, 1,  1],
    "treatment": ["A", "A", "B", "B", "A", "B", "A", "B"],
    "age":       [55, 62, 48, 71, 59, 44, 67, 53],
})
data["event"].mean()                 # 事件比例 62.5%，設限比例 37.5%

# 分析前的健全性檢查
assert (data["time"] > 0).all()      # 時間必須 > 0
assert data["event"].isin([0, 1]).all()
assert data["time"].notna().all()

# 從日期計算時間
# df["time"] = (df["end_date"] - df["start_date"]).dt.days
# df["event"] = df["death_date"].notna().astype(int)

# 模擬：Weibull 事件時間 + 隨機失去追蹤 + 行政設限
def simulate_survival(n=300, scale=18, shape=1.2, admin=36, seed=42):
    rng = np.random.default_rng(seed)
    t_true = scale * rng.weibull(shape, n)
    t_ltfu = rng.uniform(0, admin * 1.5, n)
    t_obs = np.minimum.reduce([t_true, t_ltfu, np.full(n, admin)])
    return pd.DataFrame({"time": t_obs.round(2), "event": (t_obs == t_true).astype(int)})
```

## 常見錯誤

| 錯誤 | 為什麼錯 | 修正 |
| --- | --- | --- |
| 刪除設限觀測 | 偏向較短的存活時間、丟失資訊 | 保留全部，用存活方法 |
| 把設限當成「沒發生事件」做邏輯斯迴歸 | 追蹤時間不同的人被當成一樣 | 用 KM / Cox |
| 把存活時間當一般迴歸的結果 | 忽略設限 | KM、Cox、參數存活模型 |
| 時間 = 0 | 數值問題 | 確保 T > 0（例如當天事件記為 0.5 天） |
| 事件定義模糊或中途改變 | 結果無法解讀 | 蒐集資料前就定義清楚 |
| **不朽時間偏誤 (immortal time bias)** | 把「開始治療前」的存活時間算給治療組（要先活到開始治療才會被歸為治療組），治療看起來有效 | 把治療當**時間相依共變數**，或用 landmark analysis |
| 忽略競爭風險 | 會高估累積發生率 | 用競爭風險方法（見下） |

## 競爭風險 (Competing Risks)

有多種事件、發生其中一種就**不可能**再發生另一種時（死於癌症 vs 死於心臟病），把競爭事件當設限會**高估**目標事件的累積發生率（1 − KM 不再是有意義的機率）。

| 問題 | 方法 |
| --- | --- |
| 各事件的累積發生率 | 累積發生函數 (cumulative incidence function, CIF)，Aalen-Johansen 估計量（`lifelines.AalenJohansenFitter`） |
| 共變數對事件**發生率**的影響（病因探討） | 原因別風險 (cause-specific hazard)：其他事件當設限的 Cox |
| 共變數對**累積發生率**的影響（預測） | Fine-Gray 子分配風險模型 (subdistribution hazard) |

競爭風險在醫學資料中非常常見（例如老年族群的癌症特異死亡）。
