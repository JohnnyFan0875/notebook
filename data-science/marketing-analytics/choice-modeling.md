# Choice Modeling

choice modeling 處理的是「消費者在一組 alternatives 中會選哪一個」這類問題。它比一般 binary classification 多了一層結構，因為模型不只看某個人會不會買，而是看他會在多個候選方案之間如何取捨。

Key point: choice model 的核心不是預測單一 yes/no，而是描述 **alternatives 的相對吸引力** 如何隨 price、feature、channel 或 merchandising signal 改變。

## When A Choice Model Is The Right Framing

Choice modeling 常出現在：

- 品牌選擇
- 產品設計與 feature trade-off
- pricing 與 share simulation
- merchandising placement 或 badge effect
- survey-based conjoint analysis

如果問題是：

- 顧客會不會買任一商品？偏向 binary response
- 顧客會在三台車、五個方案、十個品牌裡選哪個？偏向 choice model

## Logistic Regression Is A Special Case

對多選項問題，常見基礎模型是 **multinomial logit**。

它和一般 logistic regression 的關係可以這樣理解：

- binary logit: 兩個選項
- multinomial logit: 多個互斥選項

所以 logistic regression 可以看成 multinomial logit 的特例，而不是完全不同的東西。

## Utility Is The Hidden Layer Behind Choice

Choice models 通常假設每個選項都有一個 latent utility：

```text
utility = systematic part + random part
```

systematic part 常由可觀測特徵組成，例如：

- price
- seat count
- transmission
- convertible or not
- promotion flag

模型不是直接說「這個人一定選 A」，而是說：

- utility 較高的方案更容易被選中
- share 是各方案 utility 相對大小的結果

## Long Format Is Usually The Natural Data Structure

Choice data 常見兩種格式：

- **wide format**: 每一題或每一選項有自己的一組欄位
- **long format**: 每一列代表一個 respondent-option 組合

對建模來說，long format 通常更自然，因為它能清楚表示：

- 哪個 respondent 看到了哪些 alternatives
- 哪個 alternative 最後被選中
- 每個 alternative 的 attributes 是什麼

Tip: 如果資料最後要丟進 multinomial logit、conditional logit 或 mixed logit，long format 通常是比較穩的起點。

## Conjoint Data Is Stated Preference Data

很多 choice model 不是來自真實交易，而是來自 survey choice tasks。這類資料常叫做：

- **conjoint data**
- **stated preference data**

它的價值是：

- 可以在商品上市前測試 feature 組合
- 可以模擬現實中還不存在的產品設計
- 可以用受控方式比較 price / feature trade-off

但要注意：

- stated preference 不等於 revealed preference
- survey 裡說會選，不保證真實市場一定會買

A practical comparison:

| Data Type | What It Captures | Typical Strength | Typical Risk |
| --- | --- | --- | --- |
| Stated preference | what people say they would choose | test hypothetical products before launch | hypothetical bias |
| Revealed preference | what people actually chose | closer to real economic behavior | limited to options that were truly available |

Tip: conjoint and stated-preference studies are especially valuable when the product or offer does not exist yet. Revealed-preference data becomes more important once real market behavior can be observed.

## Multinomial Logit Is The Common Baseline

multinomial logit 的 baseline 問題通常是：

```text
Pr(choice = j) = f(attributes of alternative j relative to other alternatives)
```

在 marketing context，最常見的用途包括：

- 看 price 對 share 的影響
- 看 feature 提升能否補償價格上升
- 比較不同 product designs 的預測接受度

一個簡化版 workflow 可能長這樣：

```python
# Pseudocode structure
# one row per respondent-alternative
# columns: respondent_id, alternative_id, chosen, price, feature_1, feature_2
```

重點不是語法本身，而是每個特徵都要能被解讀成對 utility 的貢獻。

## Share Prediction Is One Of The Most Practical Outputs

Choice model 很常被拿來做 market share simulation。

典型做法是：

1. 為每個候選產品計算 utility
2. 將 utility 轉成 choice probability
3. 把各產品 probability 視為預測 share

這讓模型可以回答：

- 如果新產品價格更高，share 會掉多少？
- 加上 convertible feature 能不能補回價格劣勢？
- 哪個設計組合最有可能吃到最大 share？

Key point: choice model 的價值常不是只做分類正確率，而是支援 **what-if simulation**。

## Interactions And Segment-Specific Sensitivity Matter

不同市場區隔對價格與 features 的敏感度常不一樣。例如：

- premium segment 對 price 較不敏感
- practical segment 更重視 seat count
- 某些 feature 只有在特定 segment 才有吸引力

所以 choice model 常會加入：

- feature interactions
- price by segment interactions
- alternative-specific effects

這比只估一個全體平均 price coefficient 更貼近真正的市場異質性。

## IIA Is Useful But Limiting

multinomial logit 的經典限制之一是 **IIA** (`independence of irrelevant alternatives`)。

直覺上它表示：

- 兩個選項之間的相對 odds，不應因第三個相似選項加入而被過度扭曲

但現實市場常常不是這樣。當 alternatives 很相似時，IIA 可能過強，導致 substitution pattern 不自然。

這也是為什麼進階 choice modeling 常往下走到：

- nested logit
- random coefficients / hierarchical choice model
- Bayesian choice models

## Hierarchical And Random-Coefficient Models Capture Heterogeneity Better

如果不同受訪者的偏好差異很大，單一固定係數模型可能太粗。

更進階的做法是讓部分係數在個體間隨機變動，例如：

- price sensitivity 因人而異
- transmission preference 因人而異

這類模型的好處是：

- substitution pattern 更彈性
- 個體差異可以被保留
- share simulation 更貼近真實異質市場

代價通常是：

- 模型更難估
- 解釋與計算成本更高
- 對資料量與設計品質要求更高

## A Practical Workflow

1. 先確認問題是 binary response 還是 true multi-alternative choice。
2. 整理 alternatives、attributes、chosen indicator 與 respondent ID。
3. 優先把資料整理成 long format。
4. 先用 multinomial logit 建立 baseline。
5. 用 predicted shares 來做價格、feature 與 product design simulation。
6. 如果 IIA 或 preference heterogeneity 太強，再考慮 nested / hierarchical extensions。

## Common Mistakes

- 把多選項問題硬塞回一般 binary classification。
- 只有 respondent-level 欄位，卻沒有 alternative-level attributes。
- 用 stated preference 結果直接當成真實市場銷量。
- 只看係數顯著，不做 share simulation。
- 忽略 segment heterogeneity，誤把全體平均偏好當成所有人的偏好。

## Related Topics

- [Market Response Models](market-response-models.md)
- [Logistic Regression](../statistics/regression-analysis/logistic-regression.md)
- [Clustering](../machine-learning/unsupervised-learning/clustering/README.md)
