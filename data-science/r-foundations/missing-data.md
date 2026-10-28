[Data Science](../README.md) › [R Foundations](README.md) › 缺失值

# 缺失值 (Missing Data in R)

R 的缺值工作流：**找出藏起來的缺值 → 轉成 `NA` → 量化與視覺化缺失模式 → 再決定刪除、標記或補值**。這篇只講 R 的 `NA` 行為與 `naniar` 工具；缺失機制（MCAR / MAR / MNAR）見 [缺失資料機制](../data-manipulation-and-eda/missing-data.md)，補值方法見 [補值](../machine-learning/preprocessing/imputation.md)，pandas 版見 [pandas 缺失值](../python-foundations/pandas/missing-data.md)。

## `NA` 的行為

| 值 | 意義 | 檢查 |
| --- | --- | --- |
| `NA` | 缺值（有型別：`NA_integer_`、`NA_real_`、`NA_character_`） | `is.na()` |
| `NaN` | 無意義的數值結果（`0/0`） | `is.nan()`；`is.na(NaN)` 也是 `TRUE` |
| `NULL` | 不存在的物件，長度 0 | `is.null()` |
| `Inf` / `-Inf` | 無限大（`1/0`、`log(0)`） | `is.infinite()` / `is.finite()` |

```r
x <- c(2, NA, 5, NaN)

x == NA                 # NA NA NA NA   永遠不要這樣比
is.na(x)                # FALSE TRUE FALSE TRUE
sum(is.na(x)); mean(is.na(x))      # 缺值數、比例
mean(x)                 # NA        會傳染
mean(x, na.rm = TRUE)   # 3.5
NA > 1; NA & FALSE; NA^0          # NA, FALSE, 1   少數不傳染的例外

df[complete.cases(df), ]           # 無任何缺值的列；tidyr::drop_na(df) 同義
tidyr::drop_na(df, age)            # 只看指定欄
colSums(is.na(df))                 # 每欄缺值數
table(df$group, useNA = "ifany")   # table() 預設不列 NA
```

| 函式 | 預設處理 NA 的方式 |
| --- | --- |
| `mean()`、`sum()`、`sd()`、`max()` | 回傳 `NA`，需 `na.rm = TRUE` |
| `cor()` | 回傳 `NA`，需 `use = "complete.obs"` / `"pairwise.complete.obs"` |
| `lm()`、`glm()` | 預設 `na.action = na.omit`，**靜默刪列**；比較模型時 n 可能不同 |
| `table()` | 不列出 NA，需 `useNA = "ifany"` |
| `dplyr::filter()` | 條件為 `NA` 的列被丟掉 |
| `left_join()` | 預設 `NA` key 會互相配對（`na_matches = "never"` 關閉） |

> `lm()` 靜默刪掉含缺值的列，兩個模型的觀測數可能不同，AIC / likelihood ratio test 就不能直接比。用 `nobs(fit)` 確認，或先在同一份 complete-case 資料上擬合。

## 藏起來的缺值

真實資料常把缺值寫成 `"N/A"`、`"missing"`、`"-"`、`-99`、`999`、`0`。

```r
# 匯入時就處理
readr::read_csv("data.csv", na = c("", "NA", "N/A", "missing", "-99"))

# 匯入後：naniar
library(naniar)
df |> replace_with_na(replace = list(grade = c("N/A", "N/a"), age = -99))
df |> replace_with_na_all(condition = ~ .x %in% c("N/A", "missing", "na"))
df |> replace_with_na_if(.predicate = is.numeric, condition = ~ .x == -99)

# 或 dplyr
df |> mutate(across(where(is.numeric), \(x) na_if(x, -99)))
```

> 生資情境：蛋白質體 / 代謝體的「未偵測」常被寫成 0 或空白，但它多半是**低於偵測極限 (MNAR)**，不是隨機缺失；單細胞的 0 則是真實觀測到的 0 counts，不是 `NA`。兩者處理方式完全不同，見 [缺失資料機制](../data-manipulation-and-eda/missing-data.md)。

## 量化缺失：naniar 摘要

| 函式 | 回答 |
| --- | --- |
| `miss_var_summary(df)` | 哪些欄缺最多（數量、百分比） |
| `miss_case_summary(df)` | 哪些列缺最多 |
| `miss_var_table(df)` / `miss_case_table(df)` | 「缺 k 個值」的欄 / 列各有幾個 |
| `miss_var_span(df, var, span_every = 4000)` | 每段時間區間的缺值數 |
| `miss_var_run(df, var)` | 連續缺 / 連續有值的長度（零星 vs 整段斷訊） |
| `df \|> group_by(g) \|> miss_var_summary()` | 各組缺值比例（缺失是否與分組有關） |

```r
library(naniar)
miss_var_summary(airquality)       # Ozone 37 (24.2%), Solar.R 7 (4.58%), ...
n_miss(airquality); pct_complete_case(airquality)   # 44, 72.5
```

## 視覺化缺失模式

| 圖 | 函式 | 看什麼 |
| --- | --- | --- |
| 整體熱圖 | `vis_miss(df, cluster = TRUE)` | 缺值位置、是否成塊 |
| 每欄缺值數 | `gg_miss_var(df, facet = group)` | 哪些欄、哪些組缺 |
| 缺值組合 | `gg_miss_upset(df)` | 哪些欄常一起缺（同一檢驗套組未做） |
| 依類別 | `gg_miss_fct(df, fct = Month)` | 缺失比例是否隨組別變化 → 可能 MAR |
| 依時間 | `gg_miss_span(df, var, span_every = 3000)` | 儀器斷訊的時段 |
| 散佈圖含缺值 | `ggplot(df, aes(x, y)) + geom_miss_point()` | 缺值點放在軸下方，看它們落在哪 |

```r
library(ggplot2)
ggplot(airquality, aes(Solar.R, Ozone)) + geom_miss_point()
gg_miss_fct(airquality, fct = Month)       # 6 月 Ozone 缺最多
```

## Shadow matrix：把「是否缺失」變成欄位

`bind_shadow()` 為每欄加上一個 `_NA` 欄（值為 `!NA` / `NA`），之後可以用它 group、facet、上色，比較缺失列與非缺失列在其他變數上的分布。

```r
aq_shadow <- airquality |> bind_shadow()      # 新增 Ozone_NA、Solar.R_NA...（nabular 資料）

# Ozone 缺失時，Temp 分布是否不同？差很多 → 缺失與 Temp 有關（不是 MCAR）
aq_shadow |>
  ggplot(aes(Temp, fill = Ozone_NA)) + geom_density(alpha = 0.5)

aq_shadow |> group_by(Ozone_NA) |> summarize(mean_temp = mean(Temp))
```

## 標記補值結果

補值後要知道哪些點是補出來的，才能檢查補值有沒有扭曲分布。

```r
aq_imp <- airquality |>
  bind_shadow() |>
  add_label_shadow() |>                         # any_missing 欄：該列是否有任何缺值
  mutate(across(c(Ozone, Solar.R), \(x) if_else(is.na(x), mean(x, na.rm = TRUE), x)))

ggplot(aq_imp, aes(Temp, Ozone, color = Ozone_NA)) + geom_point()
# 平均值補值的點排成一條水平線 → 低估變異、破壞相關性
```

`impute_below()` 把缺值放在觀測範圍下方 10%，**只用於探索性畫圖**，不是分析用的補值。

```r
airquality |>
  bind_shadow() |>
  mutate(across(where(is.numeric), impute_below)) |>
  ggplot(aes(Solar.R, Ozone, color = Ozone_NA)) + geom_point()
```

## 正式補值的 R 套件

| 方法 | 套件 / 函式 | 適用 |
| --- | --- | --- |
| 多重補值 (MICE) | `mice::mice()` → `with()` → `pool()` | 推論分析，保留不確定性 |
| 隨機森林 | `missForest`、`mice(method = "rf")` | 混合型別、非線性 |
| KNN | `impute::impute.knn()`（Bioconductor） | 表現量矩陣 |
| 低於偵測極限 | `imputeLCMD`、最小值 / 2、QRILC | 蛋白質體、代謝體的 MNAR |
| 簡單補值 | `tidyr::replace_na()`、`simputation` | 探索、基準線 |

方法選擇與「補值會扭曲資料」的問題見 [補值](../machine-learning/preprocessing/imputation.md)。

## 工作流程

```
1. 找藏起來的缺值（"N/A"、-99、0）→ 轉成 NA
2. 量化：每欄 / 每列 / 每組 / 每時段缺多少
3. 視覺化模式：成塊？一起缺？隨組別或時間變？
4. 用 shadow 欄比較缺失 vs 非缺失列 → 推測 MCAR / MAR / MNAR
5. 決定：刪除 / 缺失指標 / 補值（推論用多重補值）
6. 補值後保留標記，檢查分布與相關是否被扭曲
```
