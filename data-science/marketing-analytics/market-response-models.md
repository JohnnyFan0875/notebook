# Market Response Models

market response models 用來描述市場或個體對 marketing actions 的反應，例如價格變化、展示活動、coupon、feature promotion 或競品價格改變之後，銷量或購買機率會怎麼動。

Key point: 這類模型的核心不是「把資料 fit 得更好」而已，而是把可操作的行銷槓桿轉成可解讀的 response estimate，讓 pricing、promotion 與 targeting 決策有量化依據。

## Two Common Levels Of Response

同樣叫做 response model，實際上常分成兩種分析層級：

- **aggregate sales response**: 以週、店、SKU 或 campaign period 為單位，建模銷量如何隨 price 與 promotion 變動
- **individual choice response**: 以顧客或 household 為單位，建模某次購買是否會發生，或品牌是否會被選中

這兩種問題的差別很重要，因為：

- aggregate 問題比較像 regression
- individual choice 問題比較像 binary response / choice modeling

## Aggregate Demand Often Starts With Log-Linear Models

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

## Dummy Variables Let You Quantify Promotions

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

## Interactions Matter In Promotion Analysis

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

## Carryover Effects Are Easy To Miss

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

## Individual Demand Often Becomes A Binary Response Problem

當問題改成「這次會不會購買」或「會不會選這個品牌」，分析重心就會從 sales volume 轉向 purchase probability。

一個很常見的起點是：

```text
Pr(purchase = 1) = f(price, promotion, competition)
```

這時候可以先理解 **linear probability model**，但實務上通常會進一步改用 logistic 或 probit，因為：

- 機率必須落在 `0` 到 `1`
- response 對價格的影響通常不是線性的
- 二元結果的誤差結構和 OLS 假設不同

## Relative Price Is Often More Useful Than Raw Price

在品牌選擇或競品反應裡，單看某品牌自己的價格常常不夠。更有資訊量的做法是看相對價格，例如：

```python
df["price_ratio"] = np.log(df["price_brand_a"] / df["price_brand_b"])
```

這種做法反映的是：

- 自家品牌相對競品是更便宜還是更貴
- 消費者面對的不是抽象價格，而是相對選擇

Tip: competitive choice 問題裡，relative price 通常比單獨放兩個 raw price 更貼近真正的 decision context。

## Logistic And Probit Are Response Curves, Not Just Classifiers

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

## Marginal Effects Usually Matter More Than Raw Coefficients

在 nonlinear binary response model 裡，係數本身不等於機率變化。因此比起只看 coefficient，很多商業情境更該看：

- **average marginal effects**
- predicted probability curve

例如價格係數可能是負的，但管理層真正想知道的是：

- relative price 增加 1% 左右，購買機率大致下降多少？
- display 打開後，機率上升是 1 個百分點還是 10 個百分點？

Key point: 對 binary response model，marginal effects 通常比 raw coefficient 更接近商業語言。

## Model Selection Needs Both Fit And Interpretability

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

## A Practical Workflow

1. 先明確定義 response 是 `sales volume` 還是 `purchase probability`。
2. 對 aggregate sales 先做 log-transform 與 promotion dummy 盤點。
3. 檢查是否需要 interaction 與 lagged effects。
4. 對 individual choice 問題，優先考慮 logistic / probit 而不是停在 linear probability model。
5. 用 marginal effects、predicted curves、AIC 與 ROC/AUC 一起判讀。
6. 最後把模型輸出翻成 pricing、promotion 與 targeting decision language。

## Common Mistakes

- 把 log-sales 係數直接當成絕對單位變化。
- 忽略 promotion interaction，導致效果被錯誤平均。
- 用 raw binary-response coefficient 直接解釋機率改變。
- 忽略 competitive context，只看自家價格不看相對價格。
- 加入 lag term 卻沒有確認資料頻率與行為機制是否一致。

## Related Topics

- [Regression Analysis](../statistics/regression-analysis/README.md)
- [Logistic Regression](../statistics/regression-analysis/logistic-regression.md)
- [Classification Thresholds and Calibration](../machine-learning/evaluation/classification-thresholds-and-calibration.md)
- [ROC / AUC](../machine-learning/evaluation/roc-auc.md)
