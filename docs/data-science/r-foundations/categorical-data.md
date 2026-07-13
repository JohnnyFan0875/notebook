# Categorical Data in R

R 用 factor 來表示類別資料。它看起來像字串標籤，但底層其實是整數編碼加上 levels 對照表，所以理解 factor 的結構很重要。實務上如果搭配 tidyverse，常見工作不只是建立 factor，還包括重排順序、合併稀少類別、整理多欄問卷題目，以及讓圖表順序更符合閱讀邏輯。

## Creating a Factor

```r
answers <- c("stock", "bond", "bond", "stock")
investment <- factor(answers)

investment
levels(investment)
class(investment)
```

factor 很適合表示：

- 類別標籤
- 問卷選項
- 分組欄位
- 有固定集合的狀態值

若類別本身有明確順序，例如 `Rarely < Sometimes < Often < Most of the time`，就不應該完全依賴字母排序，而要主動定義 levels。

## Levels and Integer Codes

factor 底層不是直接存字串，而是存整數代碼對應到 level：

```r
as.integer(investment)
levels(investment)
```

Key point: `as.integer(factor_x)` 取到的是 level 編碼，不是你以為的原始商業意義數值。

檢查類別資料時，通常至少要看這幾件事：

- `levels(x)`：目前有哪些類別與排序
- `table(x)` 或 `count(df, x)`：各類別出現次數
- `is.na(x)`：缺值是否很多
- 是否有本質上的順序，還是只是名目型類別

## Nominal vs Ordinal

類別資料至少可以先分成兩種：

- nominal：只有分類、沒有先後，例如職稱、城市、產品類型
- ordinal：有自然順序，例如滿意度、頻率、教育程度

這個區分很重要，因為 ordinal 資料如果維持預設字母順序，圖表和摘要都可能誤導。問卷題目尤其常見這個問題。

## Binning with cut()

連續數值常需要切成區間，這時 `cut()` 很實用：

```r
buckets <- c(0, 10, 20, 30, 40, 50)
ranking_grouped <- cut(ranking, breaks = buckets)
```

這能把連續變數轉成可分組分析的區間類別，例如：

- 分數區間
- 年齡帶
- 風險等級
- 金額級距

這種做法本質上是把連續變數轉成 ordinal 類別，方便後續做計數、交叉表、分組圖表或規則式分析。

## Reordering with forcats

`forcats` 是 tidyverse 裡處理類別資料最順手的工具。最常用的不是重新編碼，而是先把順序整理對。

### fct_relevel()

當你已經知道想要的人工順序時，用 `fct_relevel()` 最直接：

```r
survey %>%
  mutate(
    response = fct_relevel(
      response,
      "Rarely", "Sometimes", "Often", "Most of the time"
    )
  )
```

這很適合：

- Likert 題目
- 頻率題目
- 狀態流程
- 報表想固定顯示順序的欄位

### fct_reorder()

若順序要跟某個數值摘要一起變動，使用 `fct_reorder()`：

```r
job_titles_by_perc %>%
  ggplot(aes(
    x = fct_reorder(CurrentJobTitleSelect, perc_w_title),
    y = perc_w_title
  )) +
  geom_point()
```

這樣類別會依 `perc_w_title` 排序，圖表更容易閱讀。常見用途是：

- 依計數排序長條圖
- 依比例排序 dot plot
- 依平均值排序群組比較圖

### fct_rev()

有時候排序方向正確，但視覺上想把最大值放最上面或最左邊，可以再包一層 `fct_rev()`：

```r
fct_rev(fct_reorder(CurrentJobTitleSelect, perc_w_title))
```

## Collapsing and Recoding Levels

類別太多時，分析通常會先簡化。這門課總結的做法很實用：

- `fct_collapse()`：把多個 levels 合併成少數幾組
- `fct_other()`：把不重要的類別統一收進 `"Other"`
- `fct_lump_n()`：只保留前 `n` 大類別，其餘合併
- `fct_lump_prop()`：保留佔比超過門檻的類別
- `fct_recode()`：直接重新命名類別

原則是先想清楚分析問題，再決定哪些細節需要保留。不要只是因為類別太多就任意 lump，否則容易把有意義的少數群體一起消掉。

## Tidy Survey Workflow

問卷資料常把同類題目攤成很多欄，例如：

- `WorkChallengeFrequencyPolitics`
- `WorkChallengeFrequencyClarity`
- `WorkChallengeFrequencyDirtyData`

分析這類資料前，通常要先轉 long format：

```r
work_challenges <- multipleChoiceResponses %>%
  select(contains("WorkChallengeFrequency")) %>%
  pivot_longer(
    everything(),
    names_to = "work_challenge",
    values_to = "frequency"
  ) %>%
  mutate(work_challenge = str_remove(
    work_challenge,
    "WorkChallengeFrequency"
  ))
```

這個流程有三個好處：

- 同主題欄位可用同一套摘要邏輯
- 類別欄位與答案欄位分離後，較容易畫圖
- 後續 `group_by()` / `summarize()` 比寬表自然

若原始資料是字串欄位，也可以先用：

```r
df %>%
  mutate(across(where(is.character), as.factor))
```

但這只適合類別集合相對穩定的情況。若欄位還要大量清理與改寫，保留 `character` 往往更安全。

## Turning Ordered Categories into Summaries

ordinal 題目常需要轉成二元或比例摘要。例如把 `Often` 與 `Most of the time` 視為「常發生」：

```r
work_challenges %>%
  filter(!is.na(frequency)) %>%
  mutate(
    frequency = if_else(
      frequency %in% c("Most of the time", "Often"),
      1,
      0
    )
  ) %>%
  group_by(work_challenge) %>%
  summarize(perc_problem = mean(frequency))
```

這種整理方式的重點不是把 ordinal 資料硬轉數值，而是先定義明確的商業規則，再計算可解釋的比例。

## Visualization Patterns

類別圖表最常見的問題不是資料錯，而是順序和標示讓人難讀。幾個很實用的做法：

- 對 ordinal 選項先用 `fct_relevel()` 指定順序
- 對摘要後的類別用 `fct_reorder()` 依數值排序
- 類別名稱很多時，旋轉軸標籤：

```r
theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

- 比例圖表把 y 軸改成百分比：

```r
scale_y_continuous(labels = scales::percent_format())
```

- 用 `labs()` 把軸標籤改成人看得懂的文字

如果類別很多，dot plot 往往比長條圖更乾淨；如果是問卷比例，比起顯示小數 `0.176`，直接顯示 `17.6%` 可讀性高很多。

## When to Use Factors Carefully

factor 很方便，但也容易踩坑：

- 若資料只是文字標籤且還會頻繁改寫，先保留 `character` 可能更單純。
- 若有明確順序，應進一步思考是否要用 ordered factor。
- 匯入資料時若自動變 factor，要先確認這是不是你要的行為。
- 先轉 factor 再做大量字串清理，通常會讓流程變麻煩。
- 合併類別前要先確認稀少類別是否剛好是分析重點。

## Common Mistakes

- 把 factor 當成普通數字做運算。
- 看到 `as.integer()` 的輸出，就誤以為那是原始類別值。
- 沒看 `levels()` 就直接建模或排序，導致順序解讀錯誤。
- 用字母排序呈現本來有順序的問卷答案。
- 在寬表上硬做摘要，結果同主題題目無法一致比較。
- 類別太多時直接畫圖，卻沒先重排、合併或轉成比例。
