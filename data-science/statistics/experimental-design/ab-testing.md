[Statistics](../README.md) › [實驗設計](README.md) › A/B 測試

# A/B 測試 (A/B Testing)

比較現有版本與一或多個變體的**隨機化實驗**，是實驗設計在產品上最常見的應用。A/B 測試不只是「看兩個 dashboard 比 p 值」：上線前就要定好**隨機化單位、指標、停止規則、決策門檻**。

## 適用性

| 適合 | 不適合 / 要小心 |
| --- | --- |
| 比較現有體驗與提議的改變 | 流量太少，達不到有意義的樣本數 |
| 可在操作上隨機分派 | 沒有明確可檢定的假設 |
| 指標能在上線前明確定義 | 倫理上不適合隨機分派 |
| 預期效果是漸進的 | 延遲決策的機會成本太高 |
| 使用者可獨立隨機化 | **網路效應 / 外溢**：使用者互相影響（社群、雙邊市場） |
| 結果能在合理時間內觀察 | 介入改變的是整個市場或系統條件 |

> 第一個問題不是「能不能測？」而是「透過實驗得知答案，會讓決策實質變好嗎？」

## 流程

1. 定義決策、指標、變體
2. 寫出假設與**最小可偵測效果 (minimum detectable effect, MDE)**
3. 估計樣本數與停止規則，見 [樣本數與檢定力](sample-size-power.md)
4. 隨機分派使用者
5. 驗證紀錄 (logging) 與健全性檢查 (sanity checks)
6. 在**正確的分析單位**彙總指標
7. 選擇對應的統計檢定
8. 一起解讀效果量、信賴區間、商業影響

上線後才更換主要指標，屬於研究者自由度 (researcher degrees of freedom)，等同 p-hacking。

## 假設與指標定義

```text
根據 X（使用者研究），我們相信若做 Y（簡化結帳頁），
則 Z 會發生（購買比例上升），以指標 M（購買率）衡量。
```

對應統計框架：H₀ 改變不影響主要指標；H₁ 有影響（事先指定單尾或雙尾）。

**指標要包含資格規則 (eligibility)**。例如「免費試用後第二週轉換率」的分母必須明確：完成試用、第一週未訂閱、且有完整第二週可觀察的使用者。寫指標時，要寫到一個沒聽過口頭說明的分析師也能從零實作。

## 分析單位 = 隨機化單位

原始紀錄常含同一使用者的多個事件。**以使用者為單位隨機化，就要以使用者為單位分析**；把事件當獨立觀測會誇大精確度、p 值過小（[假重複](core-concepts.md#實驗單位-vs-觀測單位)）。

```python
import pandas as pd

# 二元指標：每位使用者「至少轉換一次」
user = events.groupby(["variant", "user_id"], as_index=False)["purchased"].max()
conv = user.groupby("variant")["purchased"].agg(["sum", "count"])
conv["rate"] = conv["sum"] / conv["count"]

from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
proportions_ztest(conv["sum"], conv["count"])
confint_proportions_2indep(conv.loc["B", "sum"], conv.loc["B", "count"],
                           conv.loc["A", "sum"], conv.loc["A", "count"])   # 差值的 CI
```

資料用**長格式**（每列一個單位、一欄 variant、一欄結果），比每個 variant 一欄的寬格式更容易驗證與分析。

## 指標型態決定檢定

| 指標 | 例子 | 檢定 |
| --- | --- | --- |
| 二元比例 | 註冊、點擊、購買 | 兩比例 z 檢定、卡方 |
| 連續平均 | 停留時間、每位使用者營收 | Welch t 檢定（營收高度偏態時考慮 bootstrap 或 log） |
| 比率指標 | 每 session 營收、每人點擊數 | **Delta method** 或 bootstrap |

一般選檢定邏輯見 [常用檢定](../inferential-statistics/statistical-tests.md)。

**比率指標**：每位使用者同時貢獻分子與分母，不是獨立列的簡單平均。做法：(1) 在使用者層級彙總分子與分母；(2) 計算各 variant 的比率；(3) 用考慮比率變異的方法推論。

```python
per_user = (checkout.groupby(["checkout_page", "user_id"])
                    .agg(order_value=("order_value", "sum"), page_view=("user_id", "size")))
```

## 上線後、推論前的健全性檢查

| 檢查 | 目的 |
| --- | --- |
| **樣本比例不符 (sample ratio mismatch, SRM)** | 50/50 分派卻得到 52/48？用卡方適合度檢定；顯著代表分派或紀錄出問題 |
| 可觀察特徵的平衡 | 各組使用者特徵相近 |
| 紀錄覆蓋率一致 | 某組漏記事件 |
| 資格規則正確套用 | — |
| 去除重複事件 | instrumentation 造成的重複 |
| 指標隨時間的趨勢合理 | 週間 / 週末、節日、重大事件 |

```python
from scipy.stats import chisquare
chisquare([50_812, 49_188])        # SRM 檢查：p 很小 → 先修資料，不要解讀結果
```

> 壞掉的 instrumentation 產生的顯著結果，仍然是壞證據。介入前指標異常高或低時，看似的「改善」可能只是 [趨中迴歸](../regression-analysis/simple-linear-regression.md#趨中迴歸-regression-to-the-mean)。

## 偷看與多重比較

反覆檢查顯著性、一顯著就停止（**偷看 peeking**），等同做了多次未校正的比較，偽陽性率遠超過 α。上線前就要定好：

- 固定樣本數，或
- 固定實驗期間，或
- 正式的**序列檢定 (sequential testing)** 設計（如 group sequential、always-valid p-values）

多個變體或多個主要指標時，偽陽性風險再上升，見 [多重檢定校正](../inferential-statistics/multiple-testing.md)。

> **降低變異的技巧 CUPED**：用實驗前的同一指標當共變數調整（即 ANCOVA），可大幅縮小 CI、減少所需樣本數。

## 解讀結果

1. 估計的提升 / 差異是多少？
2. 信賴區間？
3. 與「無效果」相容嗎？
4. 效果大到實務上有意義嗎？
5. 還有哪些設計或資料品質風險？

微小但精確的提升可能不重要；有意義但 CI 很寬的提升可能值得延長測試。貝氏的 A/B 測試解讀見 [貝氏 vs 頻率學派](../bayesian-statistics/bayesian-vs-frequentist.md#範例ab-測試)；行銷情境見 [Campaign Measurement](../../applied-domains/marketing-analytics/campaign-measurement.md)。
