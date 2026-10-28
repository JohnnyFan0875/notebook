[Statistics](../README.md) › 機率與分配

# 機率與分配 (Probability & Distributions)

機率是描述不確定性 (uncertainty) 的語言。[敘述統計](../descriptive-statistics/README.md) 告訴你觀察到什麼；機率告訴你「可能發生什麼、多可能」，是通往 [推論統計](../inferential-statistics/README.md) 的橋樑。

## 建議順序

```
機率基礎 → 隨機變數 → 離散 / 連續分配 → 抽樣分配與 CLT → 推論統計
                                  ↘ 最大概似估計（模型怎麼「學」參數）
                                  ↘ 蒙地卡羅與重抽樣（用模擬取代公式）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [機率基礎](probability-basics.md) | 事件運算、條件機率、貝氏定理 | 資訊如何改變機率？ |
| [隨機變數](random-variables.md) | PMF / PDF / CDF、期望值、變異數 | 如何用數字描述隨機結果？ |
| [離散分配](discrete-distributions.md) | Binomial、Poisson、Negative Binomial、Geometric、Hypergeometric | 計數資料該用哪個分配？ |
| [連續分配](continuous-distributions.md) | Normal、t、χ²、F、Exponential、Log-normal、Beta | 連續資料與檢定統計量的分配 |
| [抽樣分配與中央極限定理](sampling-distributions.md) | 抽樣分配、CLT、標準誤 | 為什麼常態分配到處都是？ |
| [最大概似估計](maximum-likelihood.md) | Likelihood、MLE、與 ML loss function 的對應 | 模型參數怎麼估？ |
| [蒙地卡羅與重抽樣](monte-carlo-simulation.md) | Monte Carlo、Bootstrap、Permutation test | 公式太難時怎麼用模擬求解？ |
