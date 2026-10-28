[Machine Learning](../README.md) › 前處理

# 前處理 (Preprocessing)

把原始資料整理成模型能穩定學習的特徵。前處理直接影響泛化、[資料洩漏](../foundations/data-leakage.md) 風險與上線可重現性，所以每一步都要放進 [Pipeline](../workflow/pipeline-basic.md)。

## 建議順序

```
切分資料 → 補值 → 類別編碼 → 離群值處理 → 縮放 → 特徵選擇
（先切！）    └──────── 全部只在訓練資料上 fit ────────┘
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Train-Test Split](train-test-split.md) | 切分比例、分層、三分法 | 資料怎麼切？切多少？ |
| [補值](imputation.md) | 單一 / 多重補值、缺失指標、KNN / Iterative | 缺失值怎麼處理才不扭曲資料？ |
| [類別編碼](categorical-encoding.md) | One-hot、Ordinal、Target encoding、Hashing | 類別變數怎麼變成數字？ |
| [離群值處理](outlier-handling.md) | 偵測規則、截尾、轉換、穩健模型 | 極端值是錯誤還是訊號？ |
| [特徵縮放](feature-scaling.md) | Standard / MinMax / Robust、哪些模型需要 | 要不要縮放？用哪一種？ |
| [特徵選擇](feature-selection.md) | Filter / Wrapper / Embedded、逐步選擇 | 哪些特徵該留下？ |

## 哪些模型需要哪些前處理

| 模型 | 縮放 | One-hot | 缺失值 |
| --- | --- | --- | --- |
| 線性 / 邏輯斯迴歸（有正則化） | **需要** | 需要 | 需補值 |
| KNN、SVM、PCA、K-Means | **需要** | 需要 | 需補值 |
| 神經網路 | **需要** | 需要（或 embedding） | 需補值 |
| 決策樹、隨機森林 | 不需要 | 低基數可用 ordinal | 新版 sklearn 可直接吃 NaN（決策樹 1.3+、隨機森林 1.4+） |
| `HistGradientBoosting`、XGBoost、LightGBM | 不需要 | 可原生處理類別 | **原生支援 NaN** |

## 常見錯誤

| 錯誤 | 後果 |
| --- | --- |
| 在整份資料上先補值或標準化，再切分 | 洩漏 |
| 名目類別直接 label encode 給線性模型 | 模型以為類別有大小順序 |
| 看到離群值就刪 | 可能刪掉最重要的訊號（罕見疾病、詐欺） |
| 用全部資料挑特徵再做 CV | 洩漏，純雜訊也能有高分 |
