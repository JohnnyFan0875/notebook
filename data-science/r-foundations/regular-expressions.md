# Regular Expressions in R

當文字資料有固定但不完全整齊的格式時，regex 是 R 裡最直接的模式描述工具。它最常出現在：

- 驗證欄位格式
- 從半結構化字串抽值
- 批次清理或改寫文字
- 從 log、API 回傳或報表列中取欄位

在 R 實務上，regex 常和 `stringr` 一起使用。

## Core `stringr` Helpers

這份課程的核心函數主要是：

- `str_detect()`：判斷是否符合模式
- `str_match()`：擷取第一個完整 match 與 capture groups
- `str_match_all()`：擷取所有 matches
- `str_replace()`：取代第一個 match
- `str_replace_all()`：取代所有 matches

例如判斷字串是否以某個字元開頭：

```r
stringr::str_detect("cat", pattern = "^c")
```

## Anchors

anchors 用來限制 match 發生的位置。

- `^`：字串開頭
- `$`：字串結尾

```r
str_match("Book", "^.")
str_match("Book", ".$")
str_match("Book", "\\.")
str_match("Book.", "\\.")
```

這幾個例子分別在說：

- `^.` 會抓第一個字元
- `.$` 會抓最後一個字元
- `\\.` 才是字面上的點號

Key point: `.` 本身是 regex 特殊字元，若要匹配真正的句點，需要 escape。

## Character Classes

character classes 用來描述「哪一類字元可以出現」。

常見例子：

- `\\d`：digit
- `\\w`：word character
- `\\s`：whitespace
- `[A-Za-z]`：英文字母
- `[\\d\\s]`：digit 或 whitespace

例如：

```r
str_match_all("Hi John_35", "\\d")
str_match_all("Hi John_35", "\\w")
str_match_all("Toy Story 3", "[\\d\\s]")
```

這類模式常用在從混合字串中拆出編號、空白、代碼或 token 類型。

## Negated Classes

很多 class 都有相反版本：

- `\\D`：非 digit
- `\\W`：非 word character
- `\\S`：非 whitespace

這在「找符合條件的字元」和「排除某類字元」之間非常好用。實務上常比手寫大範圍 class 更簡潔。

## Alternation

`|` 表示「或」：

```r
str_detect(lines, "Columbia|Pixar")
```

這會匹配包含 `Columbia` 或 `Pixar` 的字串。它很適合處理：

- 多個品牌或來源名稱
- 多種合法格式
- 同義標記或替代寫法

## Quantifiers

quantifiers 描述前一個模式可以重複幾次。

- `+`：one or more
- `*`：zero or more

像這樣的模式：

```r
"[A-Za-z]+, \\d+, \\d+"
```

可以用來匹配像 `Adam, 5, 3` 這樣的結構：

- 一串字母
- 逗號加空白
- 一串數字
- 再接另一串數字

## Capturing Groups

括號 `(...)` 會把部分 match 存成可重用的群組。

```r
str_match(
  "payload: 'Adam, 5, 3', headers: 'Auth...'",
  pattern = "([A-Za-z]+), (\\d+), (\\d+)"
)
```

回傳結果中：

- 第 1 欄是完整 match
- 第 2 欄開始是每個 capture group

這很適合把一段半結構化文字拆成欄位，例如：

- name
- attempts
- logins

## Backreferences in Replacement

capture groups 不只可用來抽值，也可在 replacement 中重組句子。

```r
str_replace(
  "payload: 'Adam, 5, 3', headers: 'Auth...'",
  pattern = "([A-Za-z]+), (\\d+), (\\d+)",
  replacement = "\\1 tried to log in \\2 times."
)
```

這裡：

- `\\1` 代表第一個 group
- `\\2` 代表第二個 group

這種寫法特別適合把原始 log line 改寫成可讀句子，或從一種命名格式轉成另一種。

## `str_match()` vs `str_detect()`

兩者常一起出現，但目的不同：

- `str_detect()`：只在意有沒有 match
- `str_match()`：在意匹配內容與 capture groups

如果你只想做 filter 或旗標欄位，`str_detect()` 通常就夠了。  
如果你想把字串拆欄，應優先想 `str_match()`。

## Building Complex Patterns with `glue`

課程第二章也強調，不一定要把長 regex 全擠成一條難讀字串。可以先組片段，再拼接：

```r
pattern <- glue::glue_collapse(c(
  "name" = "[A-Za-z]+",
  ", ",
  "attempts" = "\\d+",
  ", ",
  "logins" = "\\d+"
))
```

這種做法的價值是：

- 可讀性更高
- 較容易逐段測試
- 日後修改某一段規則比較安全

如果 pattern 很長，與其追求一行寫完，不如先命名子模式。

## `glue` for String Construction

`glue` 本身不是 regex 套件，但常和 regex workflow 一起出現，因為清理與重組文字時常需要模板字串。

```r
username <- "Adam"
glue::glue("Hi {username}")
```

它也可以處理 `NA`：

```r
glue::glue(
  "Hi {username_1} and {username_2}",
  .na = ""
)
```

這在產生訊息、標籤、或 regex replacement 後續報表字串時很方便。

## Practical Workflow

一個常見的 regex 分析流程是：

1. 先用 `str_detect()` 驗證資料大致格式
2. 用 anchors、classes、quantifiers 寫出最小可行模式
3. 用 `str_match()` 或 `str_match_all()` 取出想要的片段
4. 若 pattern 太長，用 `glue_collapse()` 或命名片段拆開
5. 需要重組文字時，再用 `str_replace()` / `str_replace_all()`

## Common Mistakes

- 忘記 escape 特殊字元，例如把 `.` 當字面句點。
- 把 `str_detect()` 當成抽值函數，結果只得到 `TRUE/FALSE`。
- capture groups 寫好了，但 replacement 忘記用 `\\1`, `\\2` 之類 backreference。
- pattern 太長還硬寫成單行，導致日後難以維護。

## Takeaways

- regex 在 R 裡通常透過 `stringr` 使用
- anchors、character classes、alternation、quantifiers 是最核心的積木
- `str_match()` 對拆欄特別重要，因為它會保留 capture groups
- `str_replace()` 可以配合 backreference 重組資訊
- 對長 pattern，先拆片段再用 `glue` 組回去，通常比硬寫一大串更穩
