# Stock Price Simulation and Volatility

當金融模型開始碰到股票價格時，最麻煩的地方通常不是公式本身，而是不確定性。價格會上下波動、報酬率分布不對稱，而且今天看起來合理的路徑，明天就可能完全改觀。

Key point: 對股票價格做模型時，重點不是預測單一路徑，而是把波動、可能區間與機率分布表達清楚。

## Why Volatility Matters

股票價格難建模，最核心的原因是 volatility。它描述的是價格或報酬率在時間上的變動程度，也直接影響:

- 價格路徑看起來有多不穩定
- 未來區間有多寬
- 同樣的 expected return 會對應多大的風險

如果模型只放 expected return，卻沒有把 volatility 放進去，結果通常會看起來過度平滑，也過度自信。

## Relative Price and Daily Return

在日資料裡，常見第一步不是直接對原始價格做分析，而是先轉成相對價格或報酬率。

常見想法包括:

- relative price: 當日價格相對於前一日價格的變化
- log return: 對價格比值取自然對數

這樣做的好處是:

- 更容易比較不同時間段的變化
- 更方便和常見的連續複利模型對接
- 後續做描述統計與模擬時較自然

## Descriptive Statistics as Model Inputs

在簡化的 stock model 裡，平均報酬與標準差常是最基本的兩個輸入。

- mean: 提供平均成長或漂移方向
- standard deviation: 提供日常波動強度

這兩個量不一定能完整描述市場，但通常足夠作為第一版 simulation model 的起點。

## Annualizing Volatility

當你從 daily return 出發時，常需要把波動度轉到年化尺度，因為很多估值、風險管理或策略比較都在年尺度上討論。

直覺上:

- 日波動度反映短期變動
- 年化波動度讓不同資產或不同模型更容易在同一尺度上比較

實務上一定要先確認你使用的時間單位是一致的，否則 mean、volatility、time horizon 會互相錯位。

## Expected Return vs. Realized Return

模型裡常會區分:

- expected return: 理論上或長期平均的報酬
- realized return: 特定樣本期間實際觀察到的報酬

這個 distinction 很重要，因為 simulation 常會用 estimated return 當作輸入，但最後產出的單一路徑只是許多可能結果之一，不應被誤當成預言。

## Simulating a Simple Stock Path

一個簡化模型的核心通常是:

1. 設定初始價格
2. 給定 expected return 與 volatility
3. 為每一天抽取一個隨機 shock
4. 用新的 shock 推進下一天價格

這種模型的價值，不在於精準預測 Apple 明天收多少，而在於幫你理解:

- 高 volatility 會讓路徑多分散
- horizon 越長，不確定性累積越快
- 一樣的平均報酬，在不同風險下會對應完全不同的 price range

## Random Normals and Lognormal Prices

許多入門 stock simulation 會先假設 log returns 近似 normal，因而讓價格本身呈現 lognormal 結構。

這個假設的好處是:

- 價格不會掉到負數
- 模型和連續複利表示法相容
- 更容易計算 price range 與 probability distribution

但它仍然只是簡化。真實市場可能有 fat tails、volatility clustering、regime shifts 等現象，不會完全服從這個框架。

## Price Ranges Instead of Point Forecasts

當模型帶入 lognormal price assumption 後，輸出最好不要只停在「最終價格會是多少」，而要往前一步問:

- 合理區間大概在哪裡
- 極端但仍 plausible 的結果有多遠
- 目前市場價格落在這個分布的哪個位置

這比單點預測更誠實，也更符合不確定性的本質。

## Cumulative vs. Density Probability

在價格機率模型裡，常會同時看到兩種觀點:

- cumulative probability: 某個價格以下的累積機率
- density probability: 某個價格附近的相對機率密度

兩者用途不同:

- cumulative view 適合回答「價格低於某門檻的機率有多大」
- density view 適合回答「哪一段區間最可能出現」

如果把這兩種圖混著看，常會誤讀模型的含義。

## What the Most Likely Price Really Means

「最可能價格」不等於「一定會發生的價格」。在連續分布裡，它比較像機率密度最高的附近區間，而不是某個神奇的精準點。

因此在做圖或報告時，與其執著於單一最可能值，不如更明確地展示:

- 中心區間
- tail risk
- 分布偏態

## Spreadsheet Modeling Still Needs Statistical Discipline

即使用的是 Google Sheets，而不是 Python 或 R，模型品質仍然取決於統計與金融概念是否一致。

至少要檢查:

- mean、volatility、time step 是否使用同一尺度
- log / exp 轉換前後是否還保持定義一致
- random function 的輸出是否真的對應你假設的分布

工具不同，不代表可以省略建模紀律。

## Common Mistakes

- 直接用價格而不是報酬率做波動推估，卻沒有先處理尺度問題
- 把單次 simulation path 當成最可能真實未來
- 年化與日化參數混用
- 只看 expected return，不看 volatility 對區間寬度的影響
- 把 lognormal convenience 當成真實市場完整描述

## Practical Reminders

- stock simulation 比較適合拿來理解風險輪廓，不適合包裝成精準預測。
- 若模型輸出看起來過度平滑，先懷疑是不是波動度或隨機項被處理得太弱。
- 一張好的 price probability 圖，通常比一個單點價格更有決策價值。
