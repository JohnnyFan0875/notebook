[Statistics](../README.md) › 敘述統計

# 敘述統計 (Descriptive Statistics)

敘述統計負責「描述手上的資料長什麼樣子」。一旦開始把結論推廣到母體，就進入 [推論統計](../inferential-statistics/README.md)。

## 建議順序

```
資料能不能用？ → 是什麼型態？ → 單一變數長怎樣？ → 兩個變數有沒有關係？
 (Data Quality)   (Data Types)     (Univariate)         (Bivariate)
```

資料品質問題會讓後面所有摘要失真；資料型態決定哪些統計量是合法的。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [資料品質](data-quality.md) | 缺失值、重複、離群值、單位與標籤 | 資料可以直接分析嗎？ |
| [資料型態與量尺](data-types.md) | NOIR 量尺、pandas dtype、編碼變數 | 這欄是什麼型態？能做哪些運算？ |
| [單變數：類別型](univariate-categorical.md) | 次數表、比例、長條圖 | 各類別分布如何？ |
| [單變數：數值型](univariate-numerical.md) | 集中、離散、形狀、資料轉換 | 中心在哪？多分散？什麼形狀？ |
| [雙變數分析](bivariate.md) | 相關係數、交叉表、分組比較 | 兩個變數有關嗎？多強？ |
