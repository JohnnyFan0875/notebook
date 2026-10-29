[Statistics](../README.md) › [實驗設計](README.md) › 干擾、偏誤與效度

# 干擾、偏誤與效度 (Confounding, Bias & Validity)

核心問題：這個研究量到的真的是我想量的嗎？（內部效度）結論能推廣到其他情境嗎？（外部效度）

## 干擾 (Confounding)

干擾變數**同時**與處理（暴露）和結果有關，製造出虛假的關係或扭曲真實效果。

```
     干擾因子 (C)
       ↙     ↘
處理 (X) ──?──▶ 結果 (Y)
```

**經典例子**：鞋子越大的孩子閱讀能力越好。干擾因子是**年齡**：年紀大的孩子腳大、閱讀也好。控制年齡後關聯消失。

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)
age = rng.normal(10, 2, 200)
df = pd.DataFrame({"age": age,
                   "shoe": 0.8 * age + rng.normal(0, 0.5, 200),
                   "reading": 3 * age + rng.normal(0, 2, 200)})

df["shoe"].corr(df["reading"])                          # ≈ 0.96：強相關
smf.ols("reading ~ shoe", data=df).fit().params          # 鞋子「效果」很大
smf.ols("reading ~ shoe + age", data=df).fit().params    # 控制年齡後 ≈ 0
```

### 處理干擾的方法

| 方法 | 適用 | 做法 |
| --- | --- | --- |
| **隨機化** | 實驗 | 已知與**未知**干擾因子隨機分散到各組 |
| 限制 (restriction) | 皆可 | 只納入干擾因子的某一水準（例如只看 50 歲以上） |
| 配對 (matching) | 觀察研究 | 依干擾因子配對病例與對照 |
| 統計調整 (adjustment) | 皆可 | 把干擾因子放進模型當共變數 |
| 分層 (stratification) | 皆可 | 在每層內分別分析，再合併（Mantel-Haenszel） |
| 傾向分數 (propensity score) | 觀察研究 | 以「接受處理的機率」配對或加權 |

> 統計調整只能處理**已測量**的干擾因子；隨機化是唯一能處理**未測量**干擾因子的方法，這是實驗優於觀察研究的核心理由。

### 生資最常見的干擾：批次效應 (Batch Effect)

不同處理批次、定序機台、日期、試劑批號造成的系統性差異。

| 情況 | 後果 | 對策 |
| --- | --- | --- |
| 批次與生物條件**完全混淆**（對照全在批次 1、處理全在批次 2） | **無法分辨**生物效果與批次效果，任何方法都救不回來 | **設計階段**就讓每批次包含各組樣本（區集化 + 隨機化） |
| 批次與條件部分交錯 | 可校正 | 把 batch 放進模型（如 DESeq2 `design = ~ batch + condition`），或 ComBat / limma `removeBatchEffect`（後者僅用於視覺化） |
| 未知的批次 | 隱藏的變異 | SVA（surrogate variable analysis）估計潛在因子 |

用 [PCA](../multivariate-analysis/pca.md) 檢查：樣本若依批次而非生物條件分群，就是警訊。完全混淆時設計矩陣不滿秩的 R 範例見 [RNA-seq 實驗設計](../../../biology/genomics/sequencing-and-analysis/workflows/rna-seq/06-exploratory-design-and-count-models.md#experimental-design)；eQTL 用 PEER factors / 表現量 PCs 移除隱藏變異，見 [eQTL](../../../biology/genomics/sequencing-and-analysis/genome-wide-analysis/eqtl.md)。

### 干擾、中介、碰撞：用 DAG 判斷該調整什麼

| 角色 | 結構 | 該不該調整 |
| --- | --- | --- |
| **干擾因子 (confounder)** | X ← C → Y | ✅ **要**調整，否則有偏 |
| **中介變數 (mediator)** | X → M → Y | ❌ 估計總效果時**不要**調整，否則會移除你想估計的部分效果 |
| **碰撞變數 (collider)** | X → K ← Y | ❌ **不要**調整；調整或依它篩選樣本會**製造**虛假關聯 |

> 碰撞偏誤的例子：只分析住院病人（住院同時受疾病 A 與疾病 B 影響）時，兩種疾病會看起來負相關（Berkson's paradox）。畫出因果圖（directed acyclic graph, DAG）再決定共變數，比「把能放的變數都放進模型」可靠。

## Simpson's Paradox

合併資料的趨勢，在分組後消失或**反轉**。經典腎結石資料：

| 結石大小 | 處理 A 治癒率 | 處理 B 治癒率 |
| --- | --- | --- |
| 小 | **93%**（81/87） | 87%（234/270） |
| 大 | **73%**（192/263） | 69%（55/80） |
| **合併** | 78%（273/350） | **83%**（289/350） |

A 在兩個子群都較好，合併後卻較差。原因：較難治的大結石病人多半接受 A；結石大小同時影響處理選擇與結果（干擾）。

```python
d = pd.DataFrame({"size": ["Small", "Small", "Large", "Large"], "trt": ["A", "B", "A", "B"],
                  "cured": [81, 234, 192, 55], "total": [87, 270, 263, 80]})
d.assign(rate=d.cured / d.total)                                    # 分層
d.groupby("trt")[["cured", "total"]].sum().pipe(lambda g: g.cured / g.total)   # 合併
```

> 真實案例：UC Berkeley 入學資料、COVID 疫苗效果報告、棒球打擊率。一定要依重要子群分層檢查。

## 偏誤類型 (Types of Bias)

偏誤是**系統性**誤差，讓估計值一致地偏離真值。與隨機誤差不同，**增加資料無法修正偏誤**。

| 偏誤 | 說明 | 預防 |
| --- | --- | --- |
| 選擇偏誤 (selection) | 基線時各組就不同（非隨機分派、非隨機抽樣） | 隨機化 |
| 流失偏誤 (attrition) | 退出者與完成者不同 | 意向治療分析 (intention-to-treat, ITT) |
| 觀察者偏誤 (observer) | 評估者知道分組而影響判讀 | 盲化 |
| 反應偏誤 (response) | 社會期望、迎合研究者 | 匿名、中性措辭 |
| 回憶偏誤 (recall) | 病例與對照回憶過去的方式不同 | 客觀紀錄、前瞻性資料 |
| 確認偏誤 (ascertainment) | 某組被更徹底地檢查 | 標準化診斷準則 |
| 霍桑效應 (Hawthorne) | 知道被觀察而改變行為 | 盲化、自然情境 |
| 存活者偏誤 (survivorship) | 只看到「存活下來」的樣本 | 納入所有起始樣本 |
| 不朽時間偏誤 (immortal time) | 把處理開始前的存活時間算給處理組 | 見 [存活分析核心概念](../survival-analysis/core-concepts.md) |
| 趨中迴歸 | 極端值重測時自然往平均靠 | 對照組 |

## 盲化 (Blinding)

| 類型 | 誰不知道分組 | 何時需要 |
| --- | --- | --- |
| 單盲 (single-blind) | 受試者 | 受試者行為可能影響結果 |
| 雙盲 (double-blind) | 受試者 + 結果評估者 | 多數臨床試驗、主觀結果 |
| 三盲 (triple-blind) | + 資料分析者 | 分析決策可能引入偏誤 |
| 開放 (open-label) | 無 | 無法盲化（如手術試驗） |

不盲化時，評估者可能不自覺地高估處理組分數；實驗室中，影像判讀、細胞計數、病理評分都應盲化。

## 效度框架 (Validity)

| 效度 | 問題 | 主要威脅 |
| --- | --- | --- |
| 內部效度 (internal) | 處理真的造成觀察到的差異嗎？ | 干擾、選擇偏誤、流失 |
| 外部效度 (external) | 結果能推廣到研究之外嗎？ | 樣本不具代表性、情境不真實 |
| 統計結論效度 (statistical conclusion) | 統計推論正確嗎？ | 檢定力不足、假設違反、多重檢定 |
| 建構效度 (construct) | 量測真的捕捉到想要的概念嗎？ | 操作化不佳、觀察者偏誤 |

**內部效度的威脅（Campbell & Stanley）**

| 威脅 | 說明 |
| --- | --- |
| 歷史 (history) | 前後測之間發生外部事件 |
| 成熟 (maturation) | 受試者隨時間自然改變 |
| 測驗效應 (testing) | 做過前測讓後測表現變好 |
| 工具 (instrumentation) | 量測工具或標準在研究中改變（例如換了定序平台） |
| 統計迴歸 | 極端基線分數自然往平均移動 |
| 選擇 (selection) | 各組基線就系統性不同 |
| 流失 (attrition) | 非隨機退出 |

> 有對照組的隨機化實驗能一次控制上述所有威脅（流失除外），這就是隨機化實驗內部效度最強的原因。

**內部 vs 外部效度的取捨**：嚴格控制的實驗室實驗內部效度高、外部效度低；真實世界的觀察研究相反。實用性試驗 (pragmatic trial) 與田野實驗 (field experiment) 嘗試兼顧，業界 A/B 測試通常自然達到這種平衡。
