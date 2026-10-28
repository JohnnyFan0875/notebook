[Statistics](../README.md) › 推論統計

# 推論統計 (Inferential Statistics)

用樣本對母體下結論。永遠無法確定，但可以**量化不確定性**，並在明確的錯誤率下做決策。

## 建議順序

```
抽樣與估計 → 信賴區間 → 假設檢定 → 多重檢定校正 → 假設檢查 → 選擇檢定 → ANOVA
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [抽樣與估計](sampling-estimation.md) | 抽樣方法、點估計、估計量的偏誤與變異 | 樣本如何代表母體？ |
| [抽樣設計與調查資料](survey-sampling.md) | R 抽樣實作、bootstrap、survey weights（`survey`） | 有權重的調查資料怎麼分析？ |
| [信賴區間](confidence-intervals.md) | 平均數 / 比例的 CI、正確解讀 | 真值可能落在哪個範圍？ |
| [假設檢定](hypothesis-testing.md) | H₀ / H₁、p 值、型一 / 型二錯誤、檢定力、效果量 | 效果是真的還是雜訊？ |
| [多重檢定校正](multiple-testing.md) | Bonferroni、Holm、FDR (Benjamini-Hochberg) | 一次做上千個檢定怎麼辦？ |
| [假設檢查](assumption-checks.md) | 常態、變異數同質、獨立性 | 檢定的前提成立嗎？ |
| [常用檢定](statistical-tests.md) | t 檢定、比例檢定、相關檢定、選擇流程 | 我該用哪個檢定？ |

### ANOVA 系列

| 筆記 | 回答的問題 |
| --- | --- |
| [ANOVA 總覽](anova-overview.md) | 三組以上的平均數如何比較？ |
| [單因子 ANOVA](one-way-anova.md) | 一個因子、多個組別 |
| [二因子 ANOVA](two-way-anova.md) | 兩個因子與交互作用 |
| [重複量數 ANOVA](repeated-measures-anova.md) | 同一受試者多次量測 |
| [事後檢定與效果量](post-hoc-effect-size.md) | 哪幾組不同？差多大？ |

> 報告 p 值時，永遠搭配**效果量**與**信賴區間**：顯著不等於重要，不顯著也不等於沒有效果。
