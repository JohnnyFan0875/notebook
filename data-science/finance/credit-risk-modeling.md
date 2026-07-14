# Credit Risk Modeling

credit risk modeling 的核心不是單純把借款人分成好人或壞人，而是估計違約風險，並把這個風險接到實際放款、拒絕、定價與資本配置決策上。

Key point: 在信用風險裡，模型分數本身不是終點。真正重要的是 `probability of default` 是否可解釋、是否夠穩、是否有校準，以及在不同 acceptance threshold 下會帶來什麼經濟後果。

## What Credit Risk Means

credit risk 指的是：

- 借款人無法完整償還借款的可能性

當借款人未按約還款時，通常稱為 `default`。對風險模型來說，最基本的任務之一就是估計：

- `PD` (`probability of default`): 某筆貸款在定義期間內違約的機率

這讓問題從二元標記，進一步變成可排序、可分層、可調 threshold 的風險分數。

在更完整的風險度量裡，PD 通常還會和另外兩個量一起出現：

- `EAD` (`exposure at default`): 違約時仍暴露在風險中的金額
- `LGD` (`loss given default`): 一旦違約，最終損失占暴露金額的比例

常見的 expected loss 拆解是：

```text
EL = PD x EAD x LGD
```

Key point: 很多 credit model 雖然直接建的是 `PD`，但實際決策往往是用它去影響 expected loss，而不是只回答「會不會違約」。

## Default Labels and Prediction Target

很多信用風險模型最後會把貸款標成：

- `1`: default
- `0`: non-default

這看起來簡單，但實務上首先要釐清：

- default 的定義是什麼
- 觀察窗多長
- 標記時間點和可用特徵時間點是否一致

如果 target definition 含糊，後面再好的模型都只是學到一個模糊標籤。

## PD Is More Useful Than a Hard Class

比起直接輸出 `default / non-default`，很多情境更需要輸出機率：

- `0.10`: 很低違約風險
- `0.40`: 有風險，但未必拒貸
- `0.90`: 高度可能違約

這是因為信用決策通常不是只有一個固定答案，而是要根據：

- 風險偏好
- 損失成本
- 核貸量目標
- 資本限制

去決定該怎麼切 threshold。

## Logistic Regression as a PD Baseline

logistic regression 是信用風險建模的典型 baseline，因為它：

- 直接輸出二元事件機率
- 解釋性通常比複雜模型更好
- 對監管或商業溝通較友善

在 credit risk 語境裡，它最自然的用途不是只看分類正確率，而是把 borrower features 映射到 `PD`。

如果你要補通用模型細節，可以再看 [machine-learning logistic regression](../machine-learning/supervised-learning/classification/logistic-regression.md)。

## Trees and Gradient Boosting

當關係明顯非線性，或特徵交互作用很多時，decision trees、boosted trees、XGBoost 常常比線性模型更有表現空間。

這些模型的優勢通常包括：

- 捕捉非線性規則
- 自然處理交互作用
- 在表格資料上往往有很強的表現

但代價是：

- 解釋性變差
- 需要更小心地檢查 calibration
- 容易只顧 ranking score，而忽略經濟決策可用性

如果你要補通用 boosting 背景，可以再看 [XGBoost](../machine-learning/supervised-learning/ensemble/xgboost.md)。

## Model Output Must Be Evaluated in Finance Terms

信用風險模型不能只停在「AUC 比較高」。因為在放款業務裡，錯誤類型的成本差很多。

典型情況是：

- false positive: 把本來不會違約的人判成高風險，可能錯失少量利潤
- false negative: 把本來會違約的人判成低風險，可能承擔大額損失

這兩者在 loss 上通常非常不對稱。

## False Negatives Are Often More Costly

在信用決策中，最危險的錯誤常是：

- `false negative`: 實際會 default，模型卻判成可接受

因為它可能代表：

- 貸款放出去了
- 利潤只拿到很少
- 本金與回收價值之間出現巨大損失

也因此，單純看 log-loss、accuracy 或 even generic classification report，仍不足以回答實際放款風險。

## Ranking Quality vs. Economic Impact

兩個模型即使都有不錯的辨識能力，也可能導致完全不同的投組結果。原因是：

- 模型把誰排進高風險區
- threshold 切在哪裡
- 被接受的貸款最終損益如何

因此在 credit risk 裡，很重要的一個思路是：

- 從 classification metrics 再往前走到 portfolio impact

例如某些誤判即使數量不多，只要落在高 loan payoff exposure 上，總體損失就可能很大。

## Classification Reports Are Only a Starting Point

`classification_report()` 之類的工具很有用，但它們只是第一層檢查。你通常仍要再問：

- default class 的 recall 夠不夠嗎？
- precision 提高是否只是因為 threshold 拉太高？
- 模型表面指標改善後，接受貸款的預期損益有沒有真的變好？

如果你只比較 macro metrics，而不回到放款結果，模型優化很容易偏離業務目標。

## ROC/AUC for Ranking

ROC / AUC 在信用風險裡有價值，因為它們可以回答：

- 模型有沒有把高風險借款人排在前面？

AUC 高通常表示排序能力較好，但要注意：

- AUC 不會直接告訴你最好的放款 threshold
- AUC 高也不保證概率校準正確
- 真實成本不對稱時，單靠 AUC 不夠

如果要補通用背景，可以再看 [ROC / AUC](../machine-learning/evaluation/roc-auc.md)。

## Calibration Matters for PD

在信用風險裡，機率本身常會直接進入決策，因此 calibration 很關鍵。

一個校準良好的模型應滿足類似這種直覺：

- 如果一群貸款平均預測 `PD = 0.12`，那它們實際 default 比例應該大致接近 `12%`

這和單純排序是不同能力：

- ranking: 誰比較危險
- calibration: 模型說 `0.25` 時，現實是不是差不多 `25%`

credit scoring、定價、資本估算、風險分層都很依賴 calibration。

如果要補通用背景，可以再看 [thresholds and calibration](../machine-learning/evaluation/classification-thresholds-and-calibration.md)。

## Class Imbalance Is Structural, Not Accidental

信用資料常常高度不平衡，因為大多數借款人本來就不會 default。

造成 imbalance 的原因不只資料自然分布，也可能來自：

- 過去業務流程已經先篩掉高風險申請
- 壞帳很快被出售或轉移
- 資料抽樣與儲存機制不一致

所以在 credit risk 裡，class imbalance 不是單純技術問題，而是資料生成機制本身的一部分。

## Acceptance Rate and Threshold Design

信用模型最典型的實務應用之一，是根據 `PD` 設定 acceptance threshold：

- 高於 threshold: reject or review
- 低於 threshold: accept

這讓模型直接影響：

- 核貸率
- portfolio default rate
- 預期收益與預期損失

acceptance rate 的問題本質上是：

- 在想維持多少放款量的同時，能承受多少違約風險？

## Threshold Is a Business Policy Lever

同一個模型，改 threshold 就可能得到完全不同的業務結果：

- threshold 降低: 接受更多貸款，也可能接受更多壞帳
- threshold 提高: 壞帳變少，但也可能犧牲大量好客戶

因此 threshold selection 不應只是數學優化，而應結合：

- risk appetite
- review capacity
- funding constraints
- product margin

一個很實務的做法是把 threshold 轉成 strategy curve 來看，也就是同時追蹤：

- `accept_rate`: 你願意通過多少申請
- `cutoff`: 對應的 PD 門檻
- `bad_rate`: 被接受貸款中的實際違約比例

這種表或曲線的價值在於，它把模型門檻直接翻譯成業務後果。你不只是問「哪個 threshold 比較準」，而是問：

- 如果多放 10% 的貸款，bad rate 會上升多少？
- 如果把壞帳率壓低，會犧牲多少核貸量？

Tip: 在信用風險裡，最佳 threshold 經常不是 `0.5`，甚至不是讓 sensitivity 和 specificity 最平衡的點，而是讓 acceptance volume、risk cost 與 margin 取得可接受折衷的點。

## A Practical Credit Risk Workflow

1. 明確定義 default 標籤與觀察期間。
2. 先建立可解釋 baseline，例如 logistic regression。
3. 再比較 tree / XGBoost 等更強模型的 ranking 能力。
4. 用 classification report、ROC/AUC、calibration 分開看不同面向。
5. 把 `PD` 接到 `EL = PD x EAD x LGD` 的風險語境。
6. 最後把 threshold 接到 acceptance rate、預期損失與 portfolio impact。

## Common Mistakes

- 把 `PD` 當成硬分類，不看機率本身的資訊。
- 只追求 AUC，卻不檢查 calibration。
- 用 generic accuracy 當主指標，忽略 default class 稀少與錯誤成本不對稱。
- threshold 固定用 `0.5`，沒有根據 acceptance target 或損失函數調整。
- 忽略資料不平衡其實反映了業務流程與樣本機制。

## Practical Reminders

- credit risk 是 classification 問題，但更像 decision problem。
- ranking 好不代表可以直接拿來 pricing 或 approval。
- 如果模型最後要用在放款，請同時檢查 discrimination、calibration 與 economic impact。
