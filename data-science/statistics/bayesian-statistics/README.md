[Statistics](../README.md) › 貝氏統計

# 貝氏統計 (Bayesian Statistics)

把機率視為**信念程度 (degree of belief)**，看到新證據就更新。不只問「H₀ 下這筆資料有多不尋常」，而是直接描述**參數本身的不確定性**。

## 建議順序

```
先驗 (Prior) → 概似 (Likelihood) → 後驗 (Posterior) → 推論與決策 → 計算（MCMC）
     ↑___________________________________________|
               後驗可成為下一輪的先驗
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [貝氏定理與核心概念](bayes-theorem.md) | 更新循環、擲硬幣範例 | 貝氏思維怎麼運作？ |
| [先驗分配](prior-distributions.md) | 資訊性 / 弱資訊性 / 無資訊、先驗預測檢查 | 怎麼把先前知識寫成分配？ |
| [概似與共軛先驗](likelihood-conjugate.md) | Beta-Binomial、Gamma-Poisson、Normal-Normal | 什麼時候後驗有公式解？ |
| [後驗推論](posterior-inference.md) | 可信區間、HDI、後驗預測、決策 | 怎麼摘要與溝通後驗？ |
| [MCMC](mcmc.md) | Metropolis-Hastings、NUTS、收斂診斷 | 算不出公式時怎麼抽樣？ |
| [貝氏 vs 頻率學派](bayesian-vs-frequentist.md) | CI vs 可信區間、p 值 vs 後驗機率 | 何時用哪個框架？ |

## 常用工具

| 套件 | 用途 |
| --- | --- |
| `scipy.stats` | 共軛情況下的先驗 / 後驗（Beta、Gamma） |
| `pymc` | 機率程式語言、MCMC |
| `arviz` | 後驗摘要、收斂診斷、視覺化 |
| `bambi` | 用公式語法寫貝氏迴歸（類似 `statsmodels` / `lme4`） |
