[Statistics](../README.md) › [推論統計](README.md) › 抽樣設計與調查資料

# 抽樣設計與調查資料分析 (Survey Sampling & Survey Data)

[抽樣與估計](sampling-estimation.md) 講抽樣方法的概念；這篇是實作：用 R 從 data frame 做各種抽樣，以及分析帶有**分層 (strata)、集群 (PSU)、權重 (weight)** 的複雜抽樣調查資料（如 NHANES）。調查資料若當成普通 data frame 直接算平均與檢定，點估計會偏、標準誤會被低估。

## 抽樣設計速查

| 設計 | 做法 | 優點 | 風險 / 注意 | R（dplyr） |
| --- | --- | --- | --- | --- |
| 簡單隨機 (simple random) | 每個單位等機率 | 分析最簡單 | 小群體可能抽不到 | `slice_sample(n = 100)` / `prop = 0.1` |
| 系統 (systematic) | 每隔 k 列取一列 | 快 | 列順序有週期或排序時會帶入偏差 | `slice(seq_len(n) * k)` |
| 分層 (stratified) | 每層各抽 | 保證各層有代表、通常降低 SE | 分層變數要事先已知 | `group_by(s) \|> slice_sample(prop = 0.1)` |
| 不等比例分層 | 各層固定筆數 | 小群體也有足夠樣本 | 樣本組成 ≠ 母體，估計母體時要加權 | `group_by(s) \|> slice_sample(n = 15)` |
| 集群 (cluster) | 先抽群（醫院、學校、地區），再抽群內 | 收集成本低 | 群內相似 → 有效樣本數變小（設計效應 > 1） | 先 `sample()` 群 ID，再 `filter()` |
| 不等機率 (weighted) | 依權重抽 | 提高稀有群體入樣機率 | 估計時要用入樣機率倒數加權 | `slice_sample(weight_by = w)` |

> 分層解決的是「代表性」，不會自動消除偏差；樣本本身有選擇偏差（例如只有回覆者），加權或 bootstrap 都修不好。偏差類型見 [抽樣與估計](sampling-estimation.md)。

## R 抽樣實作

`slice_sample()` 對 data frame 抽列，`sample()` 對向量抽值；抽樣單位是一整列觀測時用前者。

```r
library(dplyr)
set.seed(19000113)                               # 抽樣要可重現就固定 seed

# 1. 簡單隨機：以筆數或比例
coffee_ratings |> slice_sample(n = 300)
coffee_ratings |> slice_sample(prop = 0.25)

# 2. 系統抽樣：先 shuffle 再等間距取，避免列順序帶入的模式
pop_size <- nrow(coffee_ratings); n <- 5
coffee_ratings |>
  slice_sample(prop = 1) |>                      # shuffle
  slice(seq_len(n) * (pop_size %/% n))

# 3. 分層：等比例 / 各層固定筆數
coffee_ratings |> group_by(country_of_origin) |> slice_sample(prop = 0.1) |> ungroup()
coffee_ratings |> group_by(country_of_origin) |> slice_sample(n = 15) |> ungroup()

# 4. 不等機率：Taiwan 被抽中的機率加倍（不是保證抽到）
coffee_ratings |>
  mutate(w = if_else(country_of_origin == "Taiwan", 2, 1)) |>
  slice_sample(prop = 0.1, weight_by = w)

# 5. 集群：先抽 5 個國家，群內全取
countries <- sample(unique(coffee_ratings$country_of_origin), size = 5)
coffee_ratings |> filter(country_of_origin %in% countries)

# 6. 重複抽樣近似抽樣分配：1000 個 n = 30 的樣本平均
means <- replicate(1000, coffee_ratings |>
  slice_sample(n = 30) |> pull(total_cup_points) |> mean())
sd(means)                                        # ≈ 標準誤

# 7. Bootstrap：從單一樣本「放回」重抽（replace = TRUE）
boot <- replicate(1000, coffee_focus |>
  slice_sample(prop = 1, replace = TRUE) |> pull(flavor) |> mean())
quantile(boot, c(0.025, 0.975))                  # percentile 95% CI
```

| 檢查 | 做法 |
| --- | --- |
| 系統抽樣前列順序是否有結構 | `ggplot(aes(rowid, y)) + geom_point() + geom_smooth()`，有趨勢或週期就先 shuffle |
| 抽樣分配、樣本數對精度的影響 | 第 6 段改不同 `n`，比較 `sd(means)`；原理見 [抽樣分配與 CLT](../probability-and-distributions/sampling-distributions.md) |
| Bootstrap 適用條件、percentile vs BCa | [拔靴法](../probability-and-distributions/monte-carlo-simulation.md#拔靴法-bootstrap) |

## 複雜抽樣調查資料

大型調查（NHANES、NHIS、BRFSS、台灣國民營養健康調查）多採**多階段分層集群抽樣**，並刻意超額抽樣特定族群（老人、少數族裔、低收入）。資料會附三種設計變數：

| 設計變數 | NHANES 欄位 | 意義 | 忽略的後果 |
| --- | --- | --- | --- |
| 權重 (weight) | `WTINT2YR`（訪談）、`WTMEC2YR`（體檢）、`WTSAF2YR`（空腹子樣本） | 這筆樣本代表母體中多少人（入樣機率倒數，經無回應與事後分層校正） | 點估計偏向被超額抽樣的族群 |
| 分層 (strata) | `SDMVSTRA` | 抽樣時的層 | SE 通常略被高估（分層本來能降變異） |
| 集群 (PSU) | `SDMVPSU` | 第一階段抽出的群（郡 / 地區） | SE **被低估**、p 值過小（群內相關被當成獨立） |

> 選權重看分析用到的變數「最窄」來自哪個子樣本：用到體檢量測就用 MEC 權重，用到空腹血糖就用空腹子樣本權重。合併多個 2 年週期時要把權重除以週期數（例如 4 年資料用 `WTMEC2YR / 2`）。

### R：`survey` 套件

先建立 design object，所有估計都透過 `svy*` 函式，不要對原始表直接 `mean()` / `table()`。以下以 survey 4.5、NHANES 2.1.4 實跑，註解數字為實際輸出。

```r
library(survey)
library(NHANES)                                    # NHANESraw：2009–2012 兩個週期

nh <- NHANESraw |> mutate(WTMEC4YR = WTMEC2YR / 2)  # 兩個週期 → 權重除以 2
des <- svydesign(ids = ~SDMVPSU, strata = ~SDMVSTRA, nest = TRUE,
                 weights = ~WTMEC4YR, data = nh)

# 1. 類別：加權列聯表、比例、design-based 卡方
svytable(~Race1, des)                              # 加權次數（估計的母體人數）
svymean(~Race1, des, na.rm = TRUE)                 # 加權比例 + SE
svytable(~Race1 + Diabetes, des)
svychisq(~Race1 + Diabetes, des)                   # Rao-Scott 校正，不是 chisq.test()；F = 5.79、p < 0.001

# 2. 數值：平均、總量、分位數（都附 SE）
svymean(~BMI, des, na.rm = TRUE)                   # 26.63（SE 0.10）；未加權 mean(nh$BMI) = 25.65
svytotal(~DaysPhysHlthBad, des, na.rm = TRUE)
svyquantile(~BMI, des, quantiles = 0.5, na.rm = TRUE)
confint(svymean(~BMI, des, na.rm = TRUE), df = degf(des))  # 自由度 = PSU 數 − 層數 = 33

# 3. 子群體：用 subset() 或 svyby()，不要先 filter 原始資料
svymean(~BMI, subset(des, Age >= 20), na.rm = TRUE)
svyby(~BMI, ~Gender, des, svymean, na.rm = TRUE)

# 4. 迴歸
fit <- svyglm(Diabetes ~ BMI + Age + Gender, design = des, family = quasibinomial())
summary(fit)

# 5. 設計效應：複雜設計的變異 / 同樣本數簡單隨機抽樣的變異
svymean(~BMI, des, na.rm = TRUE, deff = TRUE)      # DEff 3.37：變異是簡單隨機抽樣的 3.4 倍
```

| 任務 | 普通寫法（錯） | survey 寫法 |
| --- | --- | --- |
| 比例 | `prop.table(table(x))` | `svymean(~x, des)` |
| 平均 / 中位數 | `mean(x)`、`median(x)` | `svymean()`、`svyquantile()` |
| 列聯表檢定 | `chisq.test()` | `svychisq()` |
| 兩組比較 | `t.test()` | `svyttest(y ~ g, des)` |
| 迴歸 | `glm(..., weights = w)` | `svyglm(..., design = des)` |
| 子群體 | `filter()` 後再建 design | `subset(des, ...)`、`svyby()` |

> 子群體一定要在 design 上 `subset()`：先 `filter()` 原始資料會丟掉某些 PSU / 層的資訊，SE 算錯。`glm(weights = w)` 的點估計與 `svyglm` 相同，但 SE 把權重當成「次數」，完全錯誤。

### 加權的視覺化

| 圖 | 做法 |
| --- | --- |
| 類別比例長條圖 | 先 `svymean()` / `svytable()` 算加權比例，再 `geom_col()`；條件比例用 `position = "fill"` |
| 加權趨勢線 | `geom_smooth(method = "lm", aes(weight = WTMEC4YR))`；點保留原始觀測 |
| 離散 x 軸散點（如月齡） | `geom_jitter(width = 0.3, height = 0, alpha = 0.3)` 避免重疊 |

```r
babies <- nh |> filter(AgeMonths <= 6) |> select(AgeMonths, HeadCirc, WTMEC4YR)
ggplot(babies, aes(AgeMonths, HeadCirc)) +
  geom_jitter(width = 0.3, height = 0, alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE, aes(weight = WTMEC4YR))
```

把權重映射到 `alpha` 或點大小通常不直觀；讓摘要或模型層吃權重，原始點照常畫。散點的視覺密度是**樣本**密度，不是母體密度。

## Python 對照

statsmodels 沒有 design-based 標準誤；點估計可用 `np.average(weights=)`，要正確的 SE 與 CI 用 `svy`（`samplics` 的後繼套件，`samplics` 已封存）。

```python
import numpy as np
import polars as pl
import svy

df = pl.read_csv("nhanes.csv").with_columns((pl.col("WTMEC2YR") / 2).alias("WTMEC4YR"))

bmi = df.drop_nulls("BMI")
np.average(bmi["BMI"], weights=bmi["WTMEC4YR"])   # 只有點估計，沒有正確的 SE

des = svy.Design(stratum="SDMVSTRA", psu="SDMVPSU", wgt="WTMEC4YR")
s = svy.Sample(df, des)
s.estimation.mean("BMI", drop_nulls=True)          # est、se、95% CI、cv
s.estimation.prop("Race1")
s.estimation.mean("BMI", by="Gender", drop_nulls=True)
```

| R `survey` | Python `svy` |
| --- | --- |
| `svydesign(ids=, strata=, weights=)` | `svy.Design(psu=, stratum=, wgt=)` + `svy.Sample(df, design)` |
| `svymean()` / `svytotal()` / `svyquantile()` | `s.estimation.mean()` / `.total()` / `.quantile()` |
| `svyby(~y, ~g, des, svymean)` | `s.estimation.mean("y", by="g")` |
| `svyglm()` | `s.glm` |

> `svy` 仍在快速改版（本筆記以 0.36 驗證 `mean`、`prop`、`by=`），API 可能變動；正式分析仍以 R `survey` 最成熟。

## 生醫情境

| 情境 | 要注意 |
| --- | --- |
| 盛行率（如糖尿病、高血壓） | 用加權比例與 design-based CI，否則被超額抽樣族群拉偏 |
| 族群間比較 | 用 `svyby()` 或 `svyglm()` 的交互作用，不要拆成多個子資料集各自分析 |
| 風險因子迴歸 | `svyglm`；二元結果用 `quasibinomial()` 避免非整數權重警告；干擾因子見 [干擾與偏誤](../experimental-design/confounding-bias.md) |
| 合併多個調查週期 | 權重除以週期數；確認各週期變數定義與量測方式一致 |
| 實驗室子樣本（空腹、尿液） | 換用對應子樣本權重，子群體分析用 `subset(des, ...)` |
| 用調查資料訓練 ML 模型 | 預測表現看樣本即可；若要宣稱「母體」層級的表現或校準，評估時要加權 |
| 非調查的臨床 / 世代資料 | 多半沒有抽樣權重；代表性與選擇偏差見 [干擾與偏誤](../experimental-design/confounding-bias.md#偏誤類型-types-of-bias) |

## 常見錯誤

| 錯誤 | 後果 | 修正 |
| --- | --- | --- |
| 有 `weight` 欄位卻忽略 | 點估計描述的是樣本組成，不是母體 | 建 design object，用 `svy*` |
| 只用權重、忽略 strata / PSU | SE 被低估、p 值過小 | `svydesign()` 同時給 `ids`、`strata`、`weights` |
| 對調查資料跑 `chisq.test()` / `t.test()` | 檢定假設獨立同分布，型一錯誤膨脹 | `svychisq()`、`svyttest()` |
| 先 `filter()` 子群體再建 design | 子群體 SE 錯誤 | `subset(des, ...)`、`svyby()` |
| 權重選錯（訪談 vs 體檢 vs 空腹） | 子樣本代表的母體不對 | 依「最窄」的變數來源選權重 |
| 只報加權平均、不報 SE / CI | 只完成一半分析 | 一起報 estimate、SE 或 CI |
| 用一般 CI 的 z / 大自由度 | CI 太窄 | 自由度 = PSU 數 − 層數（`degf(des)`） |
| 把 raw scatterplot 的密度當成母體密度 | 誤讀分布 | 加權摘要或加權平滑線 |
| 系統抽樣前沒檢查列順序 | 樣本帶入排序模式 | 先 shuffle |
| 以為 bootstrap 能修正有偏樣本 | bootstrap 只估變異，偏差照樣存在 | 改善抽樣設計或用加權 / 校正 |
