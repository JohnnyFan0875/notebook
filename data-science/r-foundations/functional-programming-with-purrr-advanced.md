# Functional Programming with purrr Advanced

基礎 `purrr` 重點是把 iteration 寫得穩定；進階 `purrr` 則更像是在組裝一套可重用的資料流程。這一層開始關心的不只是 `map()`，而是如何把 predicate、function operator 與巢狀 list 操作組成更乾淨的工作流。

## A More Functional View of R

這份課程反覆強調兩件事：

- everything that exists is an object
- everything that happens is a function call

在 R 裡，函數本身也可以被：

- 存進變數
- 放進 list
- 當成其他函數的輸入
- 當成函數回傳值

這就是 `purrr` 進階技巧成立的前提。

## Nested Data Is Normal

`purrr` 很常出現在處理 API 或 JSON 的場景，因為 JSON 在 R 裡通常就是巢狀 list。

像課程中的 `rstudioconf` tweet dataset 就是一個多層 list：

```r
length(rstudioconf)
length(rstudioconf[[1]])
vec_depth(rstudioconf)
```

這類檢查很實用，因為在真正開始抽欄位前，你需要先知道：

- 最外層有多少元素
- 每個元素大概長什麼樣
- 巢狀深度有多深

## `keep()` and `discard()`

當你不是要「轉換」元素，而是要「依條件篩掉或保留」元素時，用 `keep()` / `discard()` 很自然。

```r
over_30000 <- keep(visits2016, ~ sum(.x) > 30000)
under_30000 <- discard(visits2016, ~ sum(.x) > 30000)
```

可以把它們理解成 list 版本的 filter：

- `keep()` 保留符合條件的元素
- `discard()` 移除符合條件的元素

這在 list of vectors、list of data frames、或巢狀 API 回傳值上都很常用。

## Predicates as Reusable Functions

條件本身也可以先抽出來，變成可重用 predicate：

```r
limit <- as_mapper(~ sum(.x) > 30000)
over_mapper <- keep(visits2016, limit)
```

這個思路很重要。當條件開始變長，與其在每次 `keep()` / `discard()` 裡重寫，不如先命名成一個 predicate，再重複使用。

## Combining `map()` with `keep()`

課程有一個很好用的模式：先 map，再在每個子物件內做條件保留。

```r
df_list <- list(iris, airquality) %>% map(head)
map(df_list, ~ keep(.x, is.factor))
```

這代表：

- 外層 `map()` 迭代資料表
- 內層 `keep()` 保留每張表中符合條件的欄位

這種雙層 list thinking 很適合欄位探索、批次檢查和 schema 比對。

## `compact()` Removes `NULL`

當 list 中有許多 `NULL` 結果時，`compact()` 很實用：

```r
list(1, NULL, 3, 4, NULL) %>%
  compact()
```

它不是依一般條件篩選，而是專門拿掉 `NULL`。這在下列情境特別常見：

- 某些 API 回傳欄位缺失
- 某些嘗試失敗後故意回 `NULL`
- 某些步驟選擇性產出結果

## `possibly()` Plus `compact()`

一個很實務的模式是失敗時回 `NULL`，之後一次清掉：

```r
l <- list(1, 2, 3, "a")
possible_log <- possibly(log, otherwise = NULL)
map(l, possible_log) %>% compact()
```

這個 pattern 很值得記住，因為它把流程分成兩步：

1. 失敗時不要中斷，先回 `NULL`
2. 最後再用 `compact()` 清理無效結果

如果你只想保留成功輸出，而不在意完整錯誤資訊，這比 `safely()` 更輕量。

## Cleaning Safe Results with `transpose()`

對 `safely()` 產生的 list，`transpose()` 仍然是整理關鍵：

```r
map(l, safe_log) %>% transpose()
```

重點不是語法本身，而是資料結構轉換：

- 原本是每筆一個 `result/error`
- 轉成一個 results 集合和一個 errors 集合

這樣更方便後續：

- 單獨檢查失敗原因
- 批次抽取成功值
- 接著再 `compact()` 或轉成 tibble

## `flatten()` Removes One Nesting Level

當 list 只是多包了一層，不需要保留那一層結構時，可以用 `flatten()`：

```r
my_list <- list(
  list(a = 1),
  list(b = 2)
)

flatten(my_list)
```

這個操作的重點是：

- 降低一層巢狀
- 保留內部元素
- 讓後續抽值或命名更直接

它很適合在 API 整理或分批運算結果合併時做第一步結構簡化。

## `as_mapper()` Creates Reusable Mappers

公式寫法 `~ .x * 2` 很方便，但如果同一個 transformation 要重複使用，可以先轉成 mapper：

```r
mult <- as_mapper(~ .x * 2)
ten_times <- as_mapper(~ .x * 10)
map(1:5, ten_times)
```

可以把 `as_mapper()` 想成把匿名函數轉成可命名、可重複套用的 transformation object。

這在以下場景很好用：

- 同一個轉換要套到很多 list
- 想先把邏輯命名再組合
- 想把 predicate 或 mapper 傳進別的函數

## `negate()` Inverts a Predicate

當你已經有一個 predicate，只想要它的反面，不需要再重寫一次條件：

```r
under_hundred <- as_mapper(~ mean(.x) < 100)
not_under_hundred <- negate(under_hundred)
map_lgl(98:102, under_hundred)
```

`negate()` 的價值在於避免條件邏輯分散。你先寫出一個清楚的「正向條件」，再需要時反轉它。

## `partial()` Prefills Arguments

`partial()` 可以先把某些參數綁定起來，產生一個新的函數：

```r
mean_na_rm <- partial(mean, na.rm = TRUE)
lm_iris <- partial(lm, data = iris)
```

這很適合：

- 固定常用選項
- 減少重複參數
- 在 `map()` 裡傳入已配置好的函數

例如不再每次都重寫 `na.rm = TRUE`，而是先建立一個一致版本的平均函數。

## `compose()` Builds Pipelines of Functions

當你想把多個小函數組成一個可重複套用的大函數時，用 `compose()`。

課程中的模式很值得保留：

```r
tidy_iris_lm <- compose(
  as_mapper(~ dplyr::filter(.x, p.value < 0.05)),
  broom::tidy,
  partial(stats::lm, data = iris, na.action = na.fail)
)
```

這表示一個輸入公式會依序經過：

1. `lm(...)`
2. `tidy()`
3. `filter(...)`

之後就能直接：

```r
list(
  Petal.Length ~ Petal.Width,
  Petal.Width ~ Sepal.Width,
  Sepal.Width ~ Sepal.Length
) %>% map(tidy_iris_lm)
```

這是進階 `purrr` 很重要的觀念: 與其反覆貼上同一段 pipeline，不如把 pipeline 本身做成函數。

## `partial()` Plus `compose()`

這兩者常常一起用：

```r
rounded_mean <- compose(
  partial(round, digits = 2),
  partial(mean, na.rm = TRUE)
)
```

或：

```r
rounded_mean <- compose(
  partial(round, digits = 1),
  partial(mean, trim = 2, na.rm = TRUE)
)
```

好處是你可以把一個常用分析習慣變成可重複使用的單一函數，例如：

- 先算平均
- 自動忽略缺失值
- 再固定四捨五入位數

## Cleaner Code Through Reusable Components

課程中用一連串重複 `lm(...) %>% tidy() %>% filter(...)` 的例子說明，重複貼上最容易藏 typo，也最難維護。

`purrr` 的進階價值不只是少寫幾行，而是把程式拆成：

- 小而清楚的 predicate
- 可重用的 mapper
- 已經預填參數的函數
- 已經組好的函數管線

這會讓批次分析更容易檢查，也比較不會在第 4 次複製貼上時出現隱性錯字。

## Practical Workflow

進階 `purrr` 常見工作流可以整理成：

1. 先理解巢狀資料的深度與結構
2. 用 `map()` / `map_*()` 抽值或轉換
3. 用 `keep()` / `discard()` 做 predicate-based filtering
4. 用 `possibly()` / `safely()` 讓流程容錯
5. 用 `compact()` / `transpose()` / `flatten()` 清理結果結構
6. 用 `partial()`、`compose()`、`as_mapper()` 產生可重用函數

## Takeaways

- 進階 `purrr` 的核心是把 function 當成可操作物件
- `keep()`、`discard()`、`compact()` 很適合 list 清理與條件篩選
- `partial()` 能把常見參數習慣封裝起來
- `compose()` 讓整段分析 pipeline 變成單一可重用函數
- `as_mapper()` 與 `negate()` 有助於建立可命名、可重用的條件與 transformation
- 處理 JSON 或 API 回傳資料時，先理解巢狀結構，再決定何時抽值、何時降維、何時清掉失敗結果
