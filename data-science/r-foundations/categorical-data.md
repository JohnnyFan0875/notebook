[Data Science](../README.md) › [R Foundations](README.md) › 類別資料

# 類別資料 (Categorical Data: factor 與 forcats)

R 用 **factor** 表示類別：看起來像字串，底層是**整數碼 + levels 對照表**。levels 的順序決定了圖表排列、模型的參考組 (reference level) 與摘要順序，所以處理類別資料的重點多半是「把 levels 整理對」。Python 對應是 `pd.Categorical`（見 [pandas dtype 與類別](../python-foundations/pandas/dtypes-categorical-strings.md)）；量尺理論見 [資料型態與量尺](../statistics/descriptive-statistics/data-types.md)。

| 類型 | 例子 | R 表示 |
| --- | --- | --- |
| 名目 (nominal) | 組織類型、細胞類型、批次 | `factor()` |
| 順序 (ordinal) | 腫瘤分級、Likert 量表、劑量組 | `factor(..., ordered = TRUE)` 或手動排 levels |
| 區間化的連續值 | 年齡帶、表現量高 / 中 / 低 | `cut()` 產生 |

## 建立與檢查

```r
group <- factor(c("trt", "ctrl", "ctrl", "trt"))
levels(group)          # "ctrl" "trt"   預設依字母排序
as.integer(group)      # 2 1 1 2        是 level 編碼，不是原始值
table(group, useNA = "ifany")
nlevels(group)

# 指定順序；ctrl 放第一個 = 模型的參考組
group <- factor(group, levels = c("ctrl", "trt"))
relevel(group, ref = "trt")

grade <- factor(c("G2", "G1", "G3"), levels = c("G1", "G2", "G3"), ordered = TRUE)
grade < "G3"           # TRUE TRUE FALSE   ordered factor 才能比大小
```

> 參考組決定 `lm()` / `glm()` 係數的意義：`grouptrt` 的係數是「trt 相對 ctrl」。DESeq2 的 `design = ~ condition` 也一樣，忘了 relevel 會讓 log2FC 正負號顛倒。見 [類別變數編碼](../machine-learning/preprocessing/categorical-encoding.md)。

### 常見陷阱

```r
f <- factor(c("10", "5", "20"))
as.numeric(f)                  # 1 3 2   ← level 編碼，錯！
as.numeric(as.character(f))    # 10 5 20 ← 正確

sub <- droplevels(subset(df, tissue != "liver"))   # 過濾後移除空的 level
forcats::fct_na_value_to_level(f, level = "(Missing)")   # NA 變成可見類別（舊名 fct_explicit_na 已棄用）

c(factor("a"), factor("b"))    # R ≥ 4.1.0 會合併成 factor；舊版回傳整數碼
```

## 連續變數分組：`cut()`

```r
age <- c(23, 37, 45, 61, 70)
cut(age, breaks = c(0, 40, 60, Inf))                 # (0,40] (0,40] (40,60] (60,Inf] (60,Inf]
cut(age, breaks = c(0, 40, 60, Inf), right = FALSE,  # [0,40) 左閉右開
    labels = c("<40", "40-59", "60+"))
cut(age, breaks = quantile(age, 0:4 / 4), include.lowest = TRUE)  # 四分位分組
dplyr::ntile(age, 4)                                 # 等數量分 4 組，回傳整數
```

> 把連續變數切組會損失資訊與檢定力，分析時優先保留連續值；切組適合報表與視覺化。

## forcats 速查

tidyverse 的 `forcats` 函式都以 `fct_` 開頭。

| 想做 | 函式 | 例子 |
| --- | --- | --- |
| 手動指定順序 | `fct_relevel()` | Likert：`fct_relevel(x, "Rarely", "Sometimes", "Often")` |
| 依另一個數值排序 | `fct_reorder()` | 依平均表現量排基因 |
| 依出現次數排序 | `fct_infreq()` | 長條圖由多到少 |
| 依出現順序 | `fct_inorder()` | 保留檔案中的原始順序 |
| 反轉順序 | `fct_rev()` | 水平長條圖最大值放上面 |
| 合併成指定群組 | `fct_collapse()` | 把多個亞型併成大類 |
| 只留前 n 大 / 佔比門檻 | `fct_lump_n()` / `fct_lump_prop()` | 其他歸 `"Other"` |
| 指定保留哪些、其餘歸 Other | `fct_other(keep = ...)` | |
| 重新命名 | `fct_recode()` | `fct_recode(x, Control = "ctrl")` |
| NA 變成 level | `fct_na_value_to_level()` | 讓缺值出現在圖表 |
| 移除未使用 level | `fct_drop()` | 同 `droplevels()` |

```r
library(tidyverse)

survey <- survey |>
  mutate(
    response = fct_relevel(response, "Rarely", "Sometimes", "Often", "Most of the time"),
    job      = fct_lump_n(job, n = 8),                      # 只留前 8 大職稱
    tissue   = fct_collapse(tissue, gut = c("colon", "ileum", "jejunum"))
  )

job_titles |>
  ggplot(aes(x = perc, y = fct_reorder(job, perc))) +      # y 軸依 perc 排序
  geom_point() +
  scale_x_continuous(labels = scales::percent_format())
```

> 合併稀少類別前先想清楚分析問題：稀少的亞型或少數族群可能正是重點。

## 問卷 / 多欄類別：先轉 long

同一主題的題目攤成很多欄（`WorkChallengeFrequencyPolitics`、`...Clarity`、`...DirtyData`）時，先轉 long format 再用同一套摘要邏輯。

```r
work_challenges <- responses |>
  select(contains("WorkChallengeFrequency")) |>
  pivot_longer(everything(), names_to = "challenge", values_to = "frequency",
               names_prefix = "WorkChallengeFrequency") |>
  filter(!is.na(frequency))

# ordinal → 二元比例：先定義規則（Often 以上算「常發生」）
work_challenges |>
  mutate(problem = frequency %in% c("Often", "Most of the time")) |>
  group_by(challenge) |>
  summarize(perc_problem = mean(problem))
```

字串欄全部轉 factor 可用 `mutate(across(where(is.character), as.factor))`，但只適合類別集合已經固定時；還要大量清理的欄位先保留 character。reshape 細節見 [tidyr 資料重塑](data-reshaping-with-tidyr.md)。

## 常見錯誤

| 錯誤 | 後果 | 對策 |
| --- | --- | --- |
| `as.numeric(factor)` | 拿到編碼而非數值 | 先 `as.character()` |
| ordinal 用字母排序 | 圖表與摘要順序錯 | `fct_relevel()` 或 `levels =` |
| 沒設參考組 | 係數 / fold change 方向與預期相反 | `relevel()` / `fct_relevel()` |
| 過濾後殘留空 level | 圖例、`table()` 出現 0 的類別；模型報錯 | `droplevels()` |
| 先轉 factor 再做字串清理 | `str_replace` 等要反覆轉型 | 清理完再轉 factor |
| 訓練與測試 levels 不一致 | 預測時出現 new level 錯誤 | 用訓練集的 levels 建 factor |
