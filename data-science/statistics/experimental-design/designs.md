[Statistics](../README.md) › [實驗設計](README.md) › 常見設計

# 常見研究設計 (Common Designs)

設計結構決定變異如何拆解、自由度如何分配、能否偵測交互作用。選擇時先問三件事：**有幾個因子？有沒有要控制的雜訊變數？每個受試者能接受幾種處理？**

## 一、實驗設計

| 設計 | 因子數 | 區集 | 特點 | 分析 |
| --- | --- | --- | --- | --- |
| **CRD** 完全隨機設計 (completely randomized) | 1+ | 無 | 最簡單；需要實驗單位同質 | 單因子 ANOVA / t 檢定 |
| **RCBD** 隨機完全區集設計 (randomized complete block) | 1+ | 1 個雜訊變數 | 每個區集內每種處理各一次 | `y ~ trt + block` |
| **BIBD** 平衡不完全區集 (balanced incomplete block) | 1 | 1 個 | 區集放不下全部處理時；每對處理同區集出現次數相同 | 調整後的區集 ANOVA |
| **拉丁方格** (Latin square) | 1 | **2 個**雜訊變數 | 每種處理在每列、每欄各出現一次；處理數 = 列數 = 欄數 | `y ~ trt + row + col` |
| **因子設計** (factorial) | 2+ | 可選 | 所有水準組合；能偵測**交互作用** | `y ~ A * B` |
| **部分因子** (fractional factorial) | 很多 | 可選 | 只跑部分組合做篩選；高階交互作用被**混淆 (aliasing)** | 主效果篩選 |
| **交叉設計** (crossover) | 1+ | 受試者 = 區集 | 每人依序接受所有處理，中間有洗除期 | 混合模型（含期別、序列） |
| **裂區設計** (split-plot) | 2+ | 整區 = 區集 | 有些因子難以在小單位上隨機化 | 混合模型（**兩個誤差項**） |

### 選擇流程

```
幾個因子？
├─ 1 個
│   ├─ 無雜訊變數 ────────────── CRD
│   ├─ 1 個雜訊變數 ──────────── RCBD（區集放不下全部處理 → BIBD）
│   ├─ 2 個雜訊變數，數量 = 處理數 ── 拉丁方格
│   └─ 每人可接受所有處理 ──────── 交叉設計
└─ 2 個以上
    ├─ 都容易隨機化 ───────────── 完全 / 部分因子設計
    └─ 某因子難以隨機化 ────────── 裂區設計
```

> 選能回答問題的**最簡單**設計。複雜設計只有在額外結構解決了真實問題時才更好。

### Python 範例

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

rng = np.random.default_rng(7)

# RCBD：3 劑量 × 4 家醫院（醫院差異大），醫院內隨機排序
rows = []
for h, b_eff in enumerate([0, 10, -8, 5], start=1):
    for trt in rng.permutation(["Low", "Medium", "High"]):
        y = 130 + b_eff + {"Low": 0, "Medium": 5, "High": 9}[trt] + rng.normal(0, 3)
        rows.append({"block": f"H{h}", "trt": trt, "bp": y})
rcbd = pd.DataFrame(rows)
anova_lm(smf.ols("bp ~ C(trt) + C(block)", data=rcbd).fit(), typ=2)
# 每格只有 1 個觀測時無法估計 區集 × 處理 交互作用（刻意的取捨）

# 2×2 因子設計：DrugB 在高劑量有額外效果（交互作用）
means = {("A", "Low"): 100, ("A", "High"): 108, ("B", "Low"): 105, ("B", "High"): 120}
fac = pd.DataFrame([{"drug": d, "dose": s, "y": m + rng.normal(0, 5)}
                    for (d, s), m in means.items() for _ in range(5)])
fac.groupby(["drug", "dose"])["y"].mean().unstack()                 # 先看各格平均
anova_lm(smf.ols("y ~ C(drug) * C(dose)", data=fac).fit(), typ=2)

# 交叉設計：混合模型（受試者為隨機效應，加入期別效果）
# smf.mixedlm("y ~ C(trt) + C(period)", data=co, groups=co["subject"]).fit()
```

BIBD 可行性檢查：t = 處理數、k = 每區集處理數、r = 每處理重複數，則 $\lambda = r(k-1)/(t-1)$ 必須是整數（λ = 每對處理同區集出現的次數）。

### 各設計的重點注意

| 設計 | 注意 |
| --- | --- |
| CRD | 實驗單位異質時（年齡不同的動物、土壤不同的田），單位間變異全進誤差項，檢定力下降 |
| RCBD | 不是為了「多分幾組」，而是保護處理比較不受已知雜訊干擾 |
| 因子設計 | 交互作用顯著時**不要只解讀主效果**；先畫交互作用圖（線平行 = 無交互作用），見 [二因子 ANOVA](../inferential-statistics/two-way-anova.md) |
| 2ᵏ 因子 | k 個兩水準因子，2ᵏ 組合；工程、篩選實驗常用 |
| 拉丁方格 | 假設處理與兩個區集變數**都沒有交互作用** |
| 交叉設計 | 洗除期 (washout) 不足 → **殘留效應 (carryover)** 會偏誤處理比較；需要效果可逆的處理 |
| 裂區設計 | 整區因子與子區因子需要不同的誤差項；用一般二因子 ANOVA 會**誇大**整區因子的顯著性 |

| 交叉設計名詞 | 意義 |
| --- | --- |
| 期別 (period) | 給予一種處理的時段 |
| 序列 (sequence) | 處理順序（A→B 或 B→A） |
| 洗除期 (washout) | 處理之間的休息期 |
| 殘留效應 (carryover) | 前一處理的效果延續到下一期 |

## 二、流病與臨床研究設計

```
研究設計
├── 觀察性：世代（前瞻 / 回溯）、病例對照、橫斷面、縱貫
├── 實驗性：隨機對照試驗 (RCT)
└── 證據整合：系統性回顧、統合分析 (meta-analysis)
```

| 類別 | 設計 | 方向 | 特點 | 優點 | 缺點 | 經典例子 |
| --- | --- | --- | --- | --- | --- | --- |
| 觀察 | 前瞻性世代 (prospective cohort) | 往前 | 先依暴露分組，追蹤結果 | 時序清楚、回憶偏誤少 | 耗時、昂貴 | Framingham 心臟研究 |
| 觀察 | 回溯性世代 (retrospective cohort) | 用既有紀錄 | 從紀錄重建暴露與結果 | 快、便宜 | 資料品質、缺少干擾變數 | 醫院員工疫苗紀錄 vs 感染 |
| 觀察 | 病例對照 (case-control) | 往回 | 先依結果分組，回溯暴露 | **罕見疾病**有效率 | 回憶偏誤；**無法算發生率** | Doll & Hill 吸菸與肺癌 |
| 觀察 | 橫斷面 (cross-sectional) | 快照 | 暴露與結果同時量 | 快、適合盛行率 | 無時序、無法推因果 | NHANES 肥胖調查 |
| 觀察 | 縱貫 (longitudinal) | 多時點 | 同一群人重複量測 | 看個體內變化、時序 | 流失偏誤、耗資源 | Nurses' Health Study |
| 實驗 | **RCT** | 往前（隨機） | 隨機分派處理 vs 對照 | **因果推論黃金標準** | 昂貴、倫理限制、推廣性 | WHI 荷爾蒙療法試驗 |
| 整合 | 系統性回顧 (systematic review) | — | 全面蒐集並評估所有相關研究 | — | — | Cochrane 回顧 |
| 整合 | 統合分析 (meta-analysis) | — | 統計合併多個研究的結果 | 證據等級高、提高檢定力 | 受限於納入研究的品質與異質性 | Statin RCT 統合分析 |

> 依研究目的另有描述性 (descriptive)、相關性 (correlational)、解釋性 (explanatory) 設計之分：描述性與相關性設計都無法推論因果，可用於產生假設。

## 三、基因變異與臨床終點分析

評估遺傳變異（如 germline SNP）與不同臨床終點的關係時，常見的分析策略：

| 終點 | 所需資料 | 初步比較 | 調整後分析 | 視覺化 / 預測力 |
| --- | --- | --- | --- | --- |
| **發生率**（疾病風險） | 病例 vs 健康對照 | [卡方檢定](../nonparametric-methods/chi-square.md)（基因型分布） | [邏輯斯迴歸](../regression-analysis/logistic-regression.md)（調整年齡、性別等）→ OR | ROC / AUC |
| **治療反應** | 有 / 無反應（化療、標靶、放療） | 卡方檢定 | 邏輯斯迴歸（調整年齡、性別、分期） | ROC / AUC |
| **復發風險** | 復發狀態 + 追蹤時間 → 無病存活 (DFS)；起點為手術或治療開始 | 卡方檢定 | [Cox 迴歸](../survival-analysis/cox-ph-model.md) → HR | [Kaplan-Meier](../survival-analysis/kaplan-meier.md)、時間相依 ROC |
| **死亡風險** | 存活狀態 + 追蹤時間 → 整體存活 (OS)；排除非疾病死亡時改看疾病特異存活 | 卡方檢定 | Cox 迴歸 → HR | Kaplan-Meier、log-rank |

| 遺傳模型 (genetic model) | 編碼（AA / Aa / aa，a 為風險等位基因） | 假設 |
| --- | --- | --- |
| 加性 (additive) | 0 / 1 / 2 | 每多一個風險等位基因，log-odds 增加固定量；GWAS 預設 |
| 顯性 (dominant) | 0 / 1 / 1 | 帶一個就有效果 |
| 隱性 (recessive) | 0 / 0 / 1 | 需要兩個才有效果 |
| 共顯性 / 基因型 (codominant) | 類別（2 個虛擬變數） | 不假設型態 |

> 同時檢定多個 SNP 或多種遺傳模型時要做 [多重檢定校正](../inferential-statistics/multiple-testing.md)；族群分層 (population stratification) 是遺傳關聯研究的主要干擾因子，常以主成分（genotype PCs）作為共變數調整。
