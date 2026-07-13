# Cumulative Gains and Lift Curves

ROC / AUC 很適合回答「模型排序能力好不好」，但很多名單式決策其實更在意另一個問題：

- 如果我只能聯絡前 10% 的人，能抓到多少真正 target？
- 比起隨機挑選，模型讓 top segment 好了幾倍？

這就是 cumulative gains 與 lift curve 的用途。

Key point: gains / lift 不是拿來取代 AUC，而是把「排序能力」翻成更接近名單投放、審核容量、人工覆核配額的語言。

## When These Curves Matter

這類曲線特別適合：

- direct marketing
- fundraising
- fraud review queue
- collection prioritization
- lead scoring
- manual investigation capacity allocation

共同特徵是：

- 模型先輸出一個 ranking 或 score
- 真正資源只能覆蓋母體的一部分

## Cumulative Gains Curve

cumulative gains curve 的 x 軸通常是：

- 按模型分數由高到低排序後
- 你選取的母體比例

y 軸則是：

- 截至目前為止累積抓到的 target 比例

例如：

- 取前 20% 的 donor
- 若已經涵蓋 60% 的會捐款者
- 那麼 `20% -> 60%` 就是 gains curve 上的一個點

### How To Read It

- 曲線越早往上衝越好，代表高分群集中了更多 target。
- 對角線附近代表接近隨機排序。
- 若前 10% 已抓到 40% target，代表模型很適合做 top-list prioritization。

Key point: cumulative gains 回答的是「如果我只出手一部分母體，能回收多少 target coverage」。

## Lift Curve

lift 描述的是：

- 某一段被選中的人群
- target incidence 相對於整體平均 incidence 高了幾倍

公式直覺可以寫成：

\[
\text{lift} = \frac{\text{segment target rate}}{\text{overall target rate}}
\]

例如：

- 整體 target incidence = `5%`
- top decile 的 target incidence = `12.5%`

則：

\[
\text{lift} = \frac{12.5\%}{5\%} = 2.5
\]

代表在這個 segment 裡，命中率是母體平均的 `2.5` 倍。

### How To Read It

- `lift = 1` 代表和隨機挑選差不多。
- 越前面的 segment lift 越高，通常代表排序越有用。
- 若前面幾個 bucket lift 很高，但後面迅速掉到 1 附近，表示模型價值集中在最前面的少數名單。

Key point: lift 回答的是「這段名單的單位效率比平均好多少」。

## Gains vs Lift

| Curve | Main question |
| --- | --- |
| Cumulative gains | 我選前 x% 人群時，能累積抓到多少 target？ |
| Lift | 我選中的這段人群，target density 比平均高幾倍？ |

兩者都依賴 ranking，但解讀角度不同：

- gains 比較像 coverage
- lift 比較像 efficiency

## Why AUC Alone Is Not Enough

AUC 很重要，但它只是一個單一數字。

它不會直接告訴你：

- 前 5% 名單到底多有價值
- 容量限制在 20% 時該不該採用這個模型
- 和「全部都聯絡」相比，能省下多少成本

因此在 ranking 問題裡，常見工作流是：

1. 先用 AUC 比較整體排序能力
2. 再用 gains / lift 看 top segments 是否真的有業務價值

## A Profit Framing

gains / lift 很容易直接接到 profit calculation。

假設：

- population size = `N`
- 每命中一個 target 的收益 = `reward_target`
- 每接觸一個人的成本 = `cost_campaign`

若某個被選 segment 的 target incidence 因 lift 提高，則可以直接比較：

- 挑 top segment 的 profit
- 全部都做的 profit
- 完全不做的 baseline

這也是為什麼 marketing、fundraising、risk operations 很喜歡 lift：它比 AUC 更容易接到資源配置與 ROI。

## Python Examples

### Plot Cumulative Gains

```python
import scikitplot as skplt

skplt.metrics.plot_cumulative_gain(y_true, y_prob)
```

### Plot Lift Curve

```python
import scikitplot as skplt

skplt.metrics.plot_lift_curve(y_true, y_prob)
```

如果你不用 `scikit-plot`，也可以自己：

1. 依 `y_prob` 由高到低排序
2. 分 bucket 或做 cumulative scan
3. 計算 cumulative target capture 與 segment incidence

## Common Interpretation Traps

- AUC 高，不代表前 10% 名單一定最好用。
- lift 高，不代表 calibration 好。
- gains 好看，也不代表 chosen cutoff 就符合成本限制。
- 若 validation split 不貼近真實 deployment，gains / lift 也可能過度樂觀。

Warning: 這些曲線都是 ranking-based evaluation。若你的最終問題是「0.8 機率到底是不是 80%」，那還要另外看 calibration。

## Practical Checklist

在看 gains / lift 前，可以先問：

1. 真實作業一次能處理多少比例的母體？
2. 每個 false positive 與 false negative 的成本差多少？
3. 你在乎的是 coverage 還是 hit rate？
4. 模型分數是否只用來排序，而不是直接當機率溝通？

## Related Notes

- [ROC curve, AUC](roc-auc.md)
- [Classification Thresholds and Calibration](classification-thresholds-and-calibration.md)
- [Class Imbalance](class-imbalance.md)
