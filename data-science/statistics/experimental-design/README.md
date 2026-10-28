[Statistics](../README.md) › 實驗設計

# 實驗設計 (Experimental Design)

在蒐集資料**之前**規劃研究，讓資料能**有效、有效率、無偏誤**地回答研究問題。設計良好的實驗才能支持**因果**結論。設計一旦有缺陷，再好的分析也救不回來。

## 開始前要回答的問題

- 實驗單位 (experimental unit) 是什麼？有效樣本數是多少？
- 處理怎麼分派？有沒有隨機化？
- 已知的變異來源（批次、機台、日期、操作者）怎麼控制？
- 需要多少樣本才有足夠的檢定力？

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [核心概念](core-concepts.md) | 變數類型、實驗單位、假重複、實驗 vs 觀察研究 | 實驗的基本結構是什麼？ |
| [設計原則](principles.md) | 隨機化、重複、區集化、局部控制 | 什麼讓實驗有效？ |
| [常見設計](designs.md) | CRD、RCBD、因子、拉丁方格、交叉、裂區 | 哪種設計結構適合？ |
| [A/B 測試](ab-testing.md) | 產品實驗、指標、偷看、SRM | 線上實驗怎麼做？ |
| [干擾、偏誤與效度](confounding-bias.md) | 干擾因子、批次效應、各種偏誤、DAG | 哪裡會出錯、如何預防？ |
| [樣本數與檢定力](sample-size-power.md) | power analysis、效果量、經驗法則 | 需要多少樣本？ |

## 實驗 vs 觀察研究

| | 實驗 (experiment) | 觀察研究 (observational study) |
| --- | --- | --- |
| 分組方式 | 研究者**隨機**分派 | 自我選擇或自然形成 |
| 因果推論 | ✅（設計良好時） | ❌ 只有關聯（需額外假設） |
| 控制干擾 | 隨機化 | 只能統計調整（已測量的變數） |
| 可行性 | 有時不實際或不道德 | 通常較容易 |
| 例子 | RCT、A/B 測試、實驗室實驗 | 調查、世代研究、病例對照研究 |

> 無法隨機化時，準實驗 (quasi-experimental) 方法如差異中的差異 (difference-in-differences)、斷點迴歸 (regression discontinuity)、工具變數 (instrumental variables)、傾向分數 (propensity score) 屬於因果推論的進階主題。
