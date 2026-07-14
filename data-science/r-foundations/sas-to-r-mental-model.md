# SAS to R Mental Model

如果你原本習慣 SAS，轉到 R 時最需要改變的通常不是某個函式名字，而是對「session、物件、資料處理與輸出」的基本想像。

SAS 比較像用一連串 `DATA step` 與 `PROC` 去驅動分析；R 則更像在互動 session 裡建立、轉換、檢查與重用物件。

## The Biggest Shift: Everything Is an Object

在 R 裡，幾乎所有東西都是 object：

- 單一數值
- vector
- matrix
- data frame / tibble
- model output
- function return value

這和 SAS 很不一樣。SAS 使用者常把分析想成「跑一段程式產生報表」；R 使用者更常想成「把結果存成物件，之後再繼續操作」。

```r
x <- 4
y <- x * x
```

這種「先命名、再重用」的習慣，是從 SAS 轉到 R 最核心的切換之一。

## Session, Environment, and Packages

R 的工作上下文可以先粗略理解成：

- session: 目前這次分析運行的空間
- environment: 當前已經存在的物件
- packages: 這個 session 已經載入的函式集合

你可以用 `ls()` 看目前 workspace 裡有哪些物件：

```r
ls()
```

對 SAS 使用者來說，這和「目前 library / dataset 有哪些內容」不完全一樣，因為 R session 裡不只資料表，還可能存著模型、向量、清理後中間結果與摘要輸出。

## Inspection Is a Daily Habit

在 R 裡，光知道一個物件「存在」還不夠，你通常還要知道它到底是什麼型別。

最常用的檢查工具：

```r
class(x)
str(x)
dim(x)
head(x)
```

- `class()`: 物件屬於哪一類
- `str()`: 結構長什麼樣
- `dim()`: 如果是矩陣或資料框，有幾列幾欄
- `head()`: 先看前幾筆

Key point: 在 R 裡，先辨認物件型別，再決定怎麼操作，通常比先背函式名更重要。

## Data Selection Feels Different

SAS 很常透過 `DATA step`、`KEEP=`、`WHERE=` 或 `PROC` 參數控制分析資料；R 常用資料轉換 verb 先把資料變成你要的樣子。

例如欄位選取：

```r
d %>%
  select(age:test)
```

或條件篩選：

```r
daviskeep %>%
  filter(sex == "M")
```

這代表在 R 中，分析前的資料整形通常是顯式寫在 pipeline 裡，而不是分散在不同 `PROC` 的參數區。

## From PROC Thinking to Pipeline Thinking

對 SAS 使用者來說，一個很好用的對照是：

- SAS: `PROC` 常同時決定資料、分析與輸出格式
- R: 常先 `select()` / `filter()` / `group_by()`，再把整理好的資料送進函式

例如 summary statistics：

```r
daviskeep %>%
  select(weight, height, bmi) %>%
  summary()
```

分組摘要：

```r
daviskeep %>%
  group_by(sex) %>%
  summarise(across(c(weight, height, bmi), mean, na.rm = TRUE))
```

這種寫法的重點不是模仿某個 `PROC MEANS`，而是把「資料長什麼樣」和「要算什麼」分成清楚的步驟。

## Common PROC Mappings

不是每個 SAS procedure 都需要一對一替代，但可以先記住常見方向：

- `PROC UNIVARIATE` / `PROC MEANS`: `summary()`、`summarise()`、`psych::describe()`
- `PROC FREQ`: `count()`、`table()`、交叉表函式
- `PROC CORR`: `cor()` 或相關矩陣 workflow
- `PROC TTEST`: `t.test()`
- `PROC ANOVA` / `PROC GLM`: `aov()` 或更一般的模型函式
- `PROC REG`: `lm()`

重點不是死背對應表，而是先接受：R 不一定把每種分析都包成「一個 procedure = 一種工作」，而是更常回到通用物件與函式。

## Output Is Also an Object

SAS 使用者常把 output 想成報表；R 使用者更常把 output 想成下一步還能繼續操作的物件。

例如：

```r
davissmry <- daviskeep %>%
  select(weight, height, bmi) %>%
  summary()
```

這時 `davissmry` 不只是螢幕輸出，它還是一個可以檢查與 subset 的物件：

```r
class(davissmry)
is.matrix(davissmry)
dim(davissmry)
davissmry[, 1:2]
```

同樣地，`summarise()` 的結果也可以直接存起來：

```r
davissmall <- daviskeep %>%
  summarise(across(c(weight, height),
                   list(mean = ~mean(.x), sd = ~sd(.x))))

str(davissmall)
davissmall$height_mean
```

Key point: 在 R 裡，很多「輸出」其實是下一步分析的輸入。

## Model Objects Work the Same Way

模型不是報表，而是物件：

```r
davislm <- lm(height ~ weight + sex, data = daviskeep)
summary(davislm)
```

你可以：

- 看 `summary(davislm)`
- 把 `summary(davislm)` 再存成另一個物件
- 從模型物件裡抽係數、殘差、fitted values

這點對 SAS 使用者很重要，因為在 R 裡分析通常不是跑完一個 model 就結束，而是把 model object 帶到後續整理、比較或視覺化。

## Grouped Analysis Feels More Explicit

SAS 的 `BY` 思維在 R 裡通常對應到先 `group_by()`，再摘要或建模。

```r
daviskeep %>%
  group_by(sex) %>%
  summarise(mean_bmi = mean(bmi, na.rm = TRUE))
```

如果你需要分組模型，也常會先切資料、再分別 fit，而不是期待所有事情都自動在同一個 procedure 裡完成。

這一點剛開始會覺得比較手動，但換來的好處是每一步都更透明。

## Practical Migration Habits

- 先把每個中間結果命名，不要只期待最後報表。
- 養成 `class()`、`str()`、`head()` 的檢查習慣。
- 先整理資料，再分析，不要把所有條件塞進單一函式。
- 把函式輸出當成可重用 object，而不是一次性文字結果。
- 遇到 SAS `PROC` 時，先問自己要的是哪種資料轉換、哪種摘要、哪種模型，而不是急著找一個名字最像的函式。

## Common Mistakes for SAS Users

- 把 R 當成「免費版 SAS」，只想找一模一樣的 `PROC` 對照。
- 不先看 `class()` / `str()` 就直接操作物件。
- 看到輸出後不存物件，導致後面沒法重用。
- 把資料整理、摘要與模型全混在同一個大步驟裡。
- 忘記 R session 是有狀態的，重跑順序會影響物件是否存在。

## Where to Go Next

- 如果你需要補 R 的資料結構，先看 [Vectors in R](vectors.md)、[Data Frames in R](data-frames.md)、[Lists in R](lists.md)。
- 如果你想把 SAS 的資料處理心智轉成現代 R workflow，接著看 [Tidyverse Workflow in R](tidyverse-workflow.md)。
- 如果你想把 SAS 風格的統計輸出轉成可操作的模型物件，接著看 [Explanatory Modeling in R](explanatory-modeling-in-r.md)。
