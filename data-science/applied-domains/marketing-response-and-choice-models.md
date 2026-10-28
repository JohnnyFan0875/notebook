[Data Science](../README.md) › [應用領域](README.md) › 行銷反應與選擇模型

# Marketing Response and Choice Models

行銷情境的資料建模：價格、促銷、展示等**可操作的槓桿**如何改變銷量或購買機率（market response），多個選項間怎麼取捨（choice model），以及一個 campaign 到底有沒有效（campaign measurement）。可遷移的方法：log-linear / GLM、多項 logit、邊際效應、[A/B 測試](../statistics/experimental-design/ab-testing.md)。

## 概觀

### Reading Reminders

- marketing response 常常是 observational pattern，不要直接把模型係數當成 causal lift。
- 價格、促銷與展示效果通常會彼此交纏，單看一個係數很容易誤解真實商業效果。

### 與其他章節的關係

- [Regression Analysis](../statistics/regression-analysis/README.md): 很多 market response 與 choice model 都建立在線性或廣義線性模型直覺上。
- [Experimental Design](../statistics/experimental-design/README.md): 若目標是估計真正的 campaign lift，而不是相關性，實驗設計很重要。
- [Machine Learning Evaluation](../machine-learning/evaluation/README.md): 當 response model 真的進入 targeting 或 allocation 決策時，threshold、calibration 與 error cost 會變重要。

## Market Response Models

market response models 用來描述市場或個體對 marketing actions 的反應，例如價格變化、展示活動、coupon、feature promotion 或競品價格改變之後，銷量或購買機率會怎麼動。

Key point: 這類模型的核心不是「把資料 fit 得更好」而已，而是把可操作的行銷槓桿轉成可解讀的 response estimate，讓 pricing、promotion 與 targeting 決策有量化依據。

### Two Common Levels Of Response

同樣叫做 response model，實際上常分成兩種分析層級：

- **aggregate sales response**: 以週、店、SKU 或 campaign period 為單位，建模銷量如何隨 price 與 promotion 變動
- **individual choice response**: 以顧客或 household 為單位，建模某次購買是否會發生，或品牌是否會被選中

這兩種問題的差別很重要，因為：

- aggregate 問題比較像 regression
- individual choice 問題比較像 binary response / choice modeling

### Aggregate Demand Often Starts With Log-Linear Models

在 sales response 場景裡，常見做法是對銷量取對數，再用線性模型描述 price 與 promotion 的影響：

```python
import numpy as np
import statsmodels.formula.api as smf

model = smf.ols(
    "np.log(sales) ~ price + display + coupon + display_coupon",
    data=df,
).fit()
```

為什麼常對 `sales` 取 log：

- 銷量常偏右且變異大
- 乘法效果會更接近加法結構
- dummy 變數與價格係數更容易用百分比直覺解讀

Tip: 在 log-sales 模型裡，dummy variable 的係數通常代表相對變化，而不是絕對增加多少單位銷量。

### Dummy Variables Let You Quantify Promotions

在 marketing response 裡，很多重要自變數本來就是 0/1：

- 是否有 display
- 是否發 coupon
- 是否有 feature promotion
- 是否同時 display + coupon

如果模型是：

```text
log(sales) = beta0 + beta1 * display
```

那麼：

- `beta0` 對應 baseline 條件下的平均 log-sales
- `exp(beta0)` 對應 baseline 條件下的大致 sales level
- `beta1` 可以近似解讀成 display 對 sales 的比例變化

對較大的 dummy effect，更穩的轉法是：

```text
percent_change = exp(beta1) - 1
```

這比直接把 `beta1` 當百分比更安全。

### Interactions Matter In Promotion Analysis

promotion effects 很少完全可加。常見情況是：

- display 單獨有效
- coupon 單獨有效
- 兩者同時出現時，效果比相加更強或更弱

所以 interaction term 往往有價值：

```python
model = smf.ols(
    "np.log(sales) ~ price + display + coupon + display:coupon",
    data=df,
).fit()
```

Key point: 如果 promotion tools 會互相放大或互相替代，沒有 interaction 的模型可能把效果錯分到錯的變數上。

### Carryover Effects Are Easy To Miss

當週 sales 不一定只受當週價格或促銷影響。前一期活動可能留下記憶、庫存或習慣效果，因此 lagged predictors 在 marketing 很常見：

```python
df["price_lag1"] = df["price"].shift(1)
df["coupon_lag1"] = df["coupon"].shift(1)
```

這類 lag term 常用來捕捉：

- promotion 後續殘留效果
- stockpiling 後的短期需求下滑
- price change 對消費者反應的延遲

Warning: lagged terms 只有在資料頻率與行為機制合理對齊時才有意義。日資料、週資料與月資料的 carryover 解讀不能混用。

### Individual Demand Often Becomes A Binary Response Problem

當問題改成「這次會不會購買」或「會不會選這個品牌」，分析重心就會從 sales volume 轉向 purchase probability。

一個很常見的起點是：

```text
Pr(purchase = 1) = f(price, promotion, competition)
```

這時候可以先理解 **linear probability model**，但實務上通常會進一步改用 logistic 或 probit，因為：

- 機率必須落在 `0` 到 `1`
- response 對價格的影響通常不是線性的
- 二元結果的誤差結構和 OLS 假設不同

### Relative Price Is Often More Useful Than Raw Price

在品牌選擇或競品反應裡，單看某品牌自己的價格常常不夠。更有資訊量的做法是看相對價格，例如：

```python
df["price_ratio"] = np.log(df["price_brand_a"] / df["price_brand_b"])
```

這種做法反映的是：

- 自家品牌相對競品是更便宜還是更貴
- 消費者面對的不是抽象價格，而是相對選擇

Tip: competitive choice 問題裡，relative price 通常比單獨放兩個 raw price 更貼近真正的 decision context。

### Logistic And Probit Are Response Curves, Not Just Classifiers

在 marketing analytics，logistic 與 probit 不只是 generic classification methods。它們更像是在描述：

- 某個 stimulus 增加時，購買機率如何平滑改變
- 機率反應在哪些區段最敏感

logistic 常見優點：

- log-odds 解讀清楚
- coefficient 與 odds ratio 語言成熟
- 跟一般機器學習分類 workflow 容易連接

probit 常見優點：

- 在 latent utility / latent preference 的敘事下常較自然
- 和某些 choice modeling 傳統更一致

實務上兩者常會得到相近的 fitted probabilities；真正應優先比較的是：

- marginal effects 是否穩定
- 預測與排序是否足夠好
- 解釋語言是否符合團隊需要

### Marginal Effects Usually Matter More Than Raw Coefficients

在 nonlinear binary response model 裡，係數本身不等於機率變化。因此比起只看 coefficient，很多商業情境更該看：

- **average marginal effects**
- predicted probability curve

例如價格係數可能是負的，但管理層真正想知道的是：

- relative price 增加 1% 左右，購買機率大致下降多少？
- display 打開後，機率上升是 1 個百分點還是 10 個百分點？

Key point: 對 binary response model，marginal effects 通常比 raw coefficient 更接近商業語言。

### Model Selection Needs Both Fit And Interpretability

在這類模型裡，常見的比較工具包括：

- nested model comparison
- `AIC`
- backward elimination / stepwise search
- ROC / AUC for binary response discrimination

但不要只因為某個模型的 `AIC` 稍低就直接採用。還要再問：

- 係數方向是否合理？
- interaction 是否真的有商業意義？
- lag term 是否只是吸收噪音？
- 模型是否能穩定外推到新的 promotion period？

### A Practical Workflow

1. 先明確定義 response 是 `sales volume` 還是 `purchase probability`。
2. 對 aggregate sales 先做 log-transform 與 promotion dummy 盤點。
3. 檢查是否需要 interaction 與 lagged effects。
4. 對 individual choice 問題，優先考慮 logistic / probit 而不是停在 linear probability model。
5. 用 marginal effects、predicted curves、AIC 與 ROC/AUC 一起判讀。
6. 最後把模型輸出翻成 pricing、promotion 與 targeting decision language。

### Common Mistakes

- 把 log-sales 係數直接當成絕對單位變化。
- 忽略 promotion interaction，導致效果被錯誤平均。
- 用 raw binary-response coefficient 直接解釋機率改變。
- 忽略 competitive context，只看自家價格不看相對價格。
- 加入 lag term 卻沒有確認資料頻率與行為機制是否一致。

### Related Topics

- [Regression Analysis](../statistics/regression-analysis/README.md)
- [Logistic Regression](../statistics/regression-analysis/logistic-regression.md)
- [Classification Thresholds and Calibration](../machine-learning/evaluation/classification-thresholds-and-calibration.md)
- [ROC / AUC](../machine-learning/evaluation/roc-auc.md)

## Choice Modeling

choice modeling 處理的是「消費者在一組 alternatives 中會選哪一個」這類問題。它比一般 binary classification 多了一層結構，因為模型不只看某個人會不會買，而是看他會在多個候選方案之間如何取捨。

Key point: choice model 的核心不是預測單一 yes/no，而是描述 **alternatives 的相對吸引力** 如何隨 price、feature、channel 或 merchandising signal 改變。

### When A Choice Model Is The Right Framing

Choice modeling 常出現在：

- 品牌選擇
- 產品設計與 feature trade-off
- pricing 與 share simulation
- merchandising placement 或 badge effect
- survey-based conjoint analysis

如果問題是：

- 顧客會不會買任一商品？偏向 binary response
- 顧客會在三台車、五個方案、十個品牌裡選哪個？偏向 choice model

### Logistic Regression Is A Special Case

對多選項問題，常見基礎模型是 **multinomial logit**。

它和一般 logistic regression 的關係可以這樣理解：

- binary logit: 兩個選項
- multinomial logit: 多個互斥選項

所以 logistic regression 可以看成 multinomial logit 的特例，而不是完全不同的東西。

### Utility Is The Hidden Layer Behind Choice

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

### Long Format Is Usually The Natural Data Structure

Choice data 常見兩種格式：

- **wide format**: 每一題或每一選項有自己的一組欄位
- **long format**: 每一列代表一個 respondent-option 組合

對建模來說，long format 通常更自然，因為它能清楚表示：

- 哪個 respondent 看到了哪些 alternatives
- 哪個 alternative 最後被選中
- 每個 alternative 的 attributes 是什麼

Tip: 如果資料最後要丟進 multinomial logit、conditional logit 或 mixed logit，long format 通常是比較穩的起點。

### Conjoint Data Is Stated Preference Data

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

### Multinomial Logit Is The Common Baseline

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

### Share Prediction Is One Of The Most Practical Outputs

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

### Interactions And Segment-Specific Sensitivity Matter

不同市場區隔對價格與 features 的敏感度常不一樣。例如：

- premium segment 對 price 較不敏感
- practical segment 更重視 seat count
- 某些 feature 只有在特定 segment 才有吸引力

所以 choice model 常會加入：

- feature interactions
- price by segment interactions
- alternative-specific effects

這比只估一個全體平均 price coefficient 更貼近真正的市場異質性。

### IIA Is Useful But Limiting

multinomial logit 的經典限制之一是 **IIA** (`independence of irrelevant alternatives`)。

直覺上它表示：

- 兩個選項之間的相對 odds，不應因第三個相似選項加入而被過度扭曲

但現實市場常常不是這樣。當 alternatives 很相似時，IIA 可能過強，導致 substitution pattern 不自然。

這也是為什麼進階 choice modeling 常往下走到：

- nested logit
- random coefficients / hierarchical choice model
- Bayesian choice models

### Hierarchical And Random-Coefficient Models Capture Heterogeneity Better

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

### A Practical Workflow

1. 先確認問題是 binary response 還是 true multi-alternative choice。
2. 整理 alternatives、attributes、chosen indicator 與 respondent ID。
3. 優先把資料整理成 long format。
4. 先用 multinomial logit 建立 baseline。
5. 用 predicted shares 來做價格、feature 與 product design simulation。
6. 如果 IIA 或 preference heterogeneity 太強，再考慮 nested / hierarchical extensions。

### Common Mistakes

- 把多選項問題硬塞回一般 binary classification。
- 只有 respondent-level 欄位，卻沒有 alternative-level attributes。
- 用 stated preference 結果直接當成真實市場銷量。
- 只看係數顯著，不做 share simulation。
- 忽略 segment heterogeneity，誤把全體平均偏好當成所有人的偏好。

### Related Topics

- [Market Response Models](#market-response-models)
- [Logistic Regression](../statistics/regression-analysis/logistic-regression.md)
- [Clustering](../machine-learning/unsupervised-learning/clustering/README.md)

## Campaign Measurement

campaign measurement 處理的是「一個 marketing campaign 到底有沒有產生想要的商業效果」，以及這個效果應該如何被拆成 channel、funnel stage、target audience 與 tactic 層級來看。

Key point: marketing measurement 不是蒐集越多 metrics 越好，而是要先分清楚哪些是 **business-impact KPI**，哪些只是 **supporting metrics**，否則團隊很容易優化了一堆 activity signal，卻沒有真的改善業務結果。

### Marketing Analytics Starts With The Question

Marketing analytics 問題通常不是抽象的「數據告訴我什麼」，而是像這些具體決策：

- 這次 holiday campaign 有沒有提升 acquisition？
- 某個新 tactic 在這個 channel 裡有沒有優於其他 tactic？
- 如果 campaign 延長一個月，預期 ROI 會怎麼變？
- 某個國家增加 spend，是否真的改善該 channel 的結果？

這類問題很適合先回到 [Forming Analytical Questions](../data-communication/forming-analytical-questions.md) 的框架，但 marketing 場景通常還要再補上：

- campaign goal 是什麼
- target audience 是誰
- 哪個 channel 或 tactic 在 scope 內
- funnel stage 在哪裡
- 成功最後要回到哪個 business outcome

### KPI And Supporting Metrics Are Not The Same Thing

在 campaign measurement 裡，很重要的一個分層是：

- **KPI**: 用來看 marketing 是否真的影響 business
- **supporting metric**: 用來監控 tactic 或 channel health

典型差異：

| Layer | What It Is For | Examples |
| --- | --- | --- |
| KPI | judge business impact | ROI, LTV, acquisition, retention, qualified conversions |
| Supporting metric | monitor execution and optimization | CPC, CTR, engagement rate, open rate, frequency, pacing |

Practical rule:

- 每個 campaign 最好只有 `1-2` 個主 KPI
- supporting metrics 可以有很多，但它們不該取代 KPI

Warning: 如果團隊只看 click-through rate、engagement rate 或 open rate，常會把「channel 活躍」誤當成「campaign 成功」。

### Common KPI Themes In Marketing

高層常會把 marketing metrics 粗分成兩類：

- **business health**
- **marketing health**

Business health 常見指標：

- ROI
- LTV
- overall acquisition
- overall retention

Marketing health 常見指標：

- acquisition cost
- cost per click
- conversion rate
- engagement rate

Key point: 這兩類都重要，但回答的問題不同。Business health 問的是「有沒有產生真正價值」，marketing health 問的是「執行過程是否健康」。

### Funnel Stage Should Drive Metric Choice

同一個 campaign，如果在不同 funnel stage，衡量方式也應該不同。

常見三層 funnel：

- **awareness / upper funnel**: 讓更多人知道品牌
- **consideration / mid funnel**: 讓品牌進入購買候選集合
- **decision / lower funnel**: 推動實際轉換或購買

對應的 channel 與衡量直覺通常不同：

| Funnel Stage | Main Goal | Common Channels | Example Metrics |
| --- | --- | --- | --- |
| Awareness | brand exposure | TV, billboard, broad-reach display | reach, impressions, aided awareness |
| Consideration | brand evaluation | social, display, research-touch channels | engagement, site visits, branded search lift |
| Decision | direct conversion | paid search, retargeting, direct response channels | conversion, CAC, revenue, qualified leads |

Tip: 不要用 lower-funnel conversion KPI 去否定 upper-funnel activity 的價值，但也不要用 awareness metrics 假裝自己回答了 ROI 問題。

### Channel Measurement Is About Access And Observability

不同 marketing channels 的 measurement 條件不一樣。

常見差異包括：

- digital channels 通常有更細的 user-level event data
- offline channels 常較依賴 aggregated reporting
- some channels are direct, others depend on platforms or partners
- identity stitching across channels is often incomplete

這會直接影響你能不能做：

- user-level attribution
- cross-channel path analysis
- clean incremental lift evaluation

Warning: 可觀測到的 channel touchpoint 不等於完整 customer journey。measurement design 必須承認這個限制。

### Attribution Is About Credit Assignment, Not Causality By Default

當團隊問「哪個 channel 帶來轉換」時，常常其實是在問 attribution。

attribution 的核心是：

- conversion credit 要分給哪個 touchpoint
- 在 multi-channel path 下，各 channel 貢獻如何分配

但 attribution 不是自動等於 causal effect，因為：

- 某些 channel 更接近最後轉換，只是因為它們出現在旅程尾端
- 某些 channel 主要做 awareness，本來就不會拿到 last-click credit
- channel exposure 與 user intent 常常高度共變

Key point: attribution is a credit-assignment framework. It is useful operationally, but it is not the same thing as a clean causal estimate.

### Integrated Campaigns Need A Lifecycle View

integrated campaigns 通常跨多個 channels、tactics 與 funnel stages，所以不該只在 campaign 結束後看一張 summary table。

一個更實務的 lifecycle 會是：

1. **before campaign**
   - define audience
   - choose channels
   - set KPI targets
   - use predictive modeling or historical benchmarks
2. **during campaign**
   - monitor pacing
   - watch KPI vs target
   - track channel health and execution issues
3. **after campaign**
   - evaluate ROI
   - summarize cross-channel trends
   - document what to repeat, stop, or redesign

Tip: campaign measurement 最常見的失敗之一，是 campaign 開跑前沒有 target，結束後才用臨時選的 metrics 做事後解釋。

### Marketing Models Plug Into Different Campaign Questions

Campaign planning 常會連到不同分析方法：

- **audience segmentation**
  - who should receive the campaign?
  - geography, lifecycle stage, age group, product set
- **response models**
  - which segments are most likely to purchase given an offer?
  - best for discount or offer response probability
- **choice models**
  - what message, offer design, or value proposition is most attractive?
  - best for alternative comparison and share simulation
- **experimentation**
  - can we test this campaign causally?
  - if not, what observational or causal-inference alternative is realistic?

這個 mapping 很重要，因為很多團隊其實不是缺模型，而是把問題丟到錯的方法上。

### A/B Testing Is Not Always Operationally Feasible

對 integrated marketing campaign，A/B testing 不一定總是能做，原因可能包括：

- 成本太高
- channel 控制權有限
- 曝光單位難以乾淨隨機化
- spillover 或 brand effects 很強

這時候仍然可以做比較成熟的 measurement：

- pre/post with strong caveats
- matched comparisons
- quasi-experimental design
- causal inference models
- simulation based on response / choice models

這不是說 experiment 不重要，而是要承認：在 marketing 世界，measurement feasibility 本身就是設計的一部分。

### A Practical Workflow

1. 先定義 campaign goal 與 funnel stage。
2. 為每個 campaign 設定 `1-2` 個主 KPI。
3. 再補 supporting metrics 來監控 channel health。
4. 明確記錄 audience、channels、geographies 與 time window。
5. 依問題選 segmentation、response model、choice model 或 experimentation。
6. 在 campaign 中持續看 pacing，而不是等結束才分析。
7. campaign 後回到 ROI、retention, acquisition 或 LTV 層級驗證是否真的有 business impact。

### Common Mistakes

- 把 supporting metrics 當成 campaign 的最終成功指標。
- 不區分 awareness、consideration、decision 的不同衡量邏輯。
- 把 attribution 結果直接當成 causal truth。
- 沒有 pre-campaign target，導致 post-campaign 評估失焦。
- 只看單一 channel，忽略 integrated campaign 的 cross-channel interaction。

### Related Topics

- [Market Response Models](#market-response-models)
- [Choice Modeling](#choice-modeling)
- [A/B Testing](../statistics/experimental-design/ab-testing.md)
- [Forming Analytical Questions](../data-communication/forming-analytical-questions.md)
