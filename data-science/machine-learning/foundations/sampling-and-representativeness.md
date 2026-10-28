[Machine Learning](../README.md) › [基礎概念](README.md) › 抽樣與代表性

# 抽樣與代表性 (Sampling and Representativeness)

模型只能從看過的資料學習。訓練資料若不能代表上線後的情境，再強的模型也會失敗，而且**驗證分數不會告訴你**，因為驗證集通常也來自同一個有偏的來源。

## 核心概念

| 概念 | 定義 | 例子 |
| --- | --- | --- |
| 抽樣偏誤 (sampling bias) | 資料收集方式本身有偏 | 只用線上問卷，漏掉不上網的族群 |
| 選擇偏誤 (selection bias) | 某些個體較容易被納入 | 詐欺模型只用「被人工審查過」的案件訓練 |
| 分布偏移 (distribution shift) | 訓練與未來資料的分布不同 | 單一醫院訓練的模型用到其他醫院；換定序平台 |
| 共變量偏移 (covariate shift) | X 的分布變了，X→y 的關係不變 | 新族群年齡分布不同 |
| 概念漂移 (concept drift) | X→y 的關係本身變了 | 政策改變後，同樣行為代表的意義不同 |

統計上的抽樣方法與偏誤分類見 [抽樣與估計](../../statistics/inferential-statistics/sampling-estimation.md)、[偏誤類型](../../statistics/experimental-design/confounding-bias.md#偏誤類型-types-of-bias)；上線後的漂移監控見 [部署與監控](../production/deployment-and-monitoring.md)。

## 要問的問題

| 問題 | 例子 |
| --- | --- |
| 誰或什麼不在資料裡？ | 罕見疾病亞型、少數族群、極端病例 |
| 樣本能代表上線族群嗎？ | 三級醫學中心的病人比一般診所病情更重 |
| 重要的邊緣案例有被涵蓋嗎？ | 罕見但代價高的情況 |
| 資料生成過程隨時間改變了嗎？ | 診斷標準、檢驗儀器、業務規則更新 |
| 標籤是怎麼產生的？ | 只有被檢驗的人才有診斷結果 → 未檢驗者不是「陰性」 |

## 問卷資料的陷阱

問卷樣本常被過濾兩次：**誰被邀請**、**誰實際回覆**。樣本可以很大，卻仍然不具代表性。

| 陷阱 | 說明 |
| --- | --- |
| 無回應偏誤 (non-response bias) | 重點不是回應率高低，而是**未回應者是否與回應者系統性不同**（不滿意的顧客不填滿意度調查） |
| 涵蓋不足 (undercoverage) | 只發線上表單 → 年長或較少上網的族群看不到 |

> 無回應不只是「少了幾列」，它會改變樣本組成，扭曲後續所有估計。

```python
import pandas as pd

# 1. 比較母體與樣本的子群比例
comparison = pd.concat([
    population["gender"].value_counts(normalize=True).rename("population"),
    sample["gender"].value_counts(normalize=True).rename("sample"),
], axis=1)
comparison["gap"] = comparison["sample"] - comparison["population"]

# 2. 分層抽樣：每個子群各抽 10%
strat_sample = population.groupby("gender").sample(frac=0.1, random_state=42)
```

重要子群的差距大時，樣本可能撐不起整體推論，需要重新設計收集方式或加權。

| 做法 | 處理的問題 | 時機 |
| --- | --- | --- |
| 分層 / 配額抽樣 (stratified / quota sampling) | 控制**誰進入樣本** | 收集時 |
| 加權 (weighting) | 調整每筆觀測在分析中的**影響力** | 分析時 |

> 在收集時就確保代表性，比事後靠加權補救可靠；加權救不了完全沒被抽到的族群。

## ML 中的對應做法

| 做法 | 說明 |
| --- | --- |
| 分層切分 | `train_test_split(..., stratify=y)`、`StratifiedKFold`，見 [Train-Test Split](../preprocessing/train-test-split.md) |
| 子群體評估 | 分別報告各族群、各醫院、各批次的效能，不只看整體平均 |
| 外部驗證 | 用不同來源的資料測試，見 [泛化](generalization.md) |
| 樣本權重 | 多數 sklearn 模型的 `fit(..., sample_weight=w)` |

> 資料涵蓋不足，無法單靠更好的演算法解決。
