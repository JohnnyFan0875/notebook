[Statistics](../README.md) › [實驗設計](README.md) › 核心概念

# 核心概念與名詞 (Core Concepts & Terminology)

很多實驗設計錯誤來自概念混淆：把干擾變數當控制變數、把觀測單位當實驗單位，都會導致分析錯誤。存活分析的資料結構見 [存活分析核心概念](../survival-analysis/core-concepts.md)。

## 變數類型

| 類型 | 定義 | 例子（藥物試驗） | 怎麼處理 |
| --- | --- | --- | --- |
| 自變數 (independent variable, IV) | 研究者操弄的「因」 | 劑量 0 / 10 / 20 mg | 隨機分派 |
| 依變數 (dependent variable, DV) | 量測的「果」 | 治療後血壓 | — |
| **干擾變數 (confounder)** | 同時影響 IV 與 DV，**扭曲**效果 | 年齡（影響劑量選擇與血壓） | **隨機化**；觀察研究只能統計調整 |
| 雜訊變數 (nuisance variable) | 影響 DV 但不是研究重點，只**增加變異** | 實驗技術員、時段、定序批次 | **區集化**或放進模型 |
| 區集變數 (blocking variable) | 用設計控制的雜訊變數 | 多中心試驗的醫院 | 每個區集內都有所有處理 |
| 共變數 (covariate) | 與處理一起量測，用來降低誤差 | 治療前基線血壓 | ANCOVA、迴歸調整 |

> **干擾 vs 雜訊**：干擾變數會造成**偏誤**（危險）；雜訊變數只增加**變異**（降低檢定力）。前者靠隨機化，後者靠區集化。

## 實驗單位 vs 觀測單位

| 名詞 | 定義 | 例子 |
| --- | --- | --- |
| **實驗單位 (experimental unit, EU)** | **獨立**接受處理的最小單位 | 接受藥物的病人、一隻小鼠、一盤培養皿 |
| 觀測單位 (observational unit, OU) | 實際被量測的單位 | 該病人的血液樣本、小鼠的每個細胞 |

**EU ≠ OU 時**：對一頭牛給處理、量 5 次牛奶，EU 是牛、OU 是牛奶樣本。把 n = 5 當獨立樣本就是**假重複 (pseudoreplication)**，會嚴重低估 SE。

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
data = pd.DataFrame({
    "cow_id": np.repeat([1, 2, 3], 5),                 # 3 個實驗單位
    "treatment": np.repeat(["A", "B", "A"], 5),
    "milk_yield": rng.normal(20, 2, 15),               # 每頭 5 次量測
})

len(data)                                              # ❌ n = 15
eu = data.groupby(["cow_id", "treatment"], as_index=False)["milk_yield"].mean()
len(eu)                                                # ✅ n = 3，先彙總到 EU 層級
# 或保留所有量測，用混合模型：milk_yield ~ treatment + (1 | cow_id)
```

### 生物實驗中的重複

| 類型 | 定義 | 用途 | 能否當作 n？ |
| --- | --- | --- | --- |
| **生物重複 (biological replicate)** | 不同個體 / 獨立培養的樣本 | 推論到母體、估計生物變異 | ✅ |
| 技術重複 (technical replicate) | 同一樣本重複量測（同一 RNA 跑兩次） | 估計量測誤差 | ❌ 先平均 |
| 細胞 / 讀值 | 同一樣本內的大量觀測 | — | ❌ |

單細胞資料比較組別時，有效樣本數是**捐贈者 / 小鼠數**，不是細胞數。見 [假設檢查：獨立性](../inferential-statistics/assumption-checks.md#獨立性-independence)、[混合效應模型](../regression-analysis/mixed-effects-models.md)。

## 因子、水準與處理

| 名詞 | 定義 | 例子 |
| --- | --- | --- |
| 因子 (factor) | 研究的類別自變數 | 藥物種類 |
| 水準 (level) | 因子的具體取值 | A、B、安慰劑 |
| 處理 (treatment) | 施加的水準組合 | 藥物 A 10 mg |
| 對照組 (control) | 比較基準 | 安慰劑組、未處理組、vehicle control |
| 安慰劑 (placebo) | 外觀相同但無效的處理 | 糖錠 |

單因子：藥物（3 水準）→ 3 組。兩因子：藥物（3）× 劑量（2）→ 6 個處理組合。**完全因子設計 (full factorial)** 測試所有組合，能偵測交互作用，見 [常見設計](designs.md)。

## 觀察研究的類型

| 類型 | 說明 | 例子 | 能估計 |
| --- | --- | --- | --- |
| 橫斷面 (cross-sectional) | 單一時間點快照 | 今天的收入與健康調查 | 盛行率、關聯 |
| 世代 (cohort) | 追蹤一群人往前看 | 追蹤吸菸者 vs 非吸菸者 10 年 | 發生率、相對風險 (RR) |
| 病例對照 (case-control) | 比較有結果 vs 無結果者的過去暴露 | 肺癌病人 vs 健康者 | **只能估 odds ratio** |
| 回溯性 (retrospective) | 使用既有紀錄回頭看 | 過去 5 年病歷 | 依設計而定 |

> **Bradford Hill 準則**用來判斷觀察到的關聯是否可能為因果：關聯強度、一致性、**時序性（因必須在果之前）**、劑量反應、生物合理性等。

## 檢查資料的實驗結構

整潔資料 (tidy data)：一列一個觀測、每個因子與結果各一欄。

```python
d = pd.DataFrame({
    "subject_id": range(1, 19),
    "drug":  np.repeat(["DrugA", "DrugB"], 9),
    "dose":  np.tile(["Low", "Medium", "High"], 6),
    "block": np.repeat([1, 2, 3], 6),
    "bp":    rng.normal(130, 10, 18).round(1),
})
d.groupby(["drug", "dose"]).size().unstack()          # 每格樣本數：是否平衡、有無缺格
pd.crosstab(d["block"], d["drug"])                    # 處理是否與區集 / 批次混在一起
```

**平衡設計 (balanced design)**：每格重複數相同，分析較簡單、檢定力較高，規劃時應盡量達成。

## 內部 vs 外部效度

| 效度 | 問題 |
| --- | --- |
| 內部效度 (internal validity) | 處理**真的造成**本研究觀察到的效果嗎？ |
| 外部效度 (external validity) | 結果能推廣到研究情境之外嗎？ |

控制越嚴格通常內部效度越高，但可能降低真實性。完整的效度與偏誤類型見 [干擾、偏誤與效度](confounding-bias.md)。
