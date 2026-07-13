# String Distance and Fuzzy Matching in R

regex 很適合描述明確規則，但真實世界常有另一類問題：字串不是「符不符合規則」，而是「有多接近」。這時候就會進到 string distance 與 fuzzy matching。

常見場景：

- 使用者拼錯名稱
- 公司、城市、藥物名有多種寫法
- 兩份資料表要做近似 join
- OCR、人工輸入或 legacy 系統帶來小錯字

## What a String Distance Means

string distance 是把兩個字串差異量化成一個數值。

```r
stringdist::stringdist("saturday", "sunday", method = "lv")
```

距離越小，通常代表越相似。  
距離為 0，代表完全相同。

重要性不在於公式本身，而在於你要先決定：

- 什麼類型的錯字最常出現
- 你需要的是嚴格比對還是近似比對

## Levenshtein Family

課程先介紹編輯距離類方法：

- `lv`：regular Levenshtein
- `dl`：Damerau-Levenshtein
- `osa`：Optimal String Alignment

```r
stringdist::stringdist(a, b, method = "lv")
stringdist::stringdist(a, b, method = "dl")
stringdist::stringdist(a, b, method = "osa")
```

這些方法大致都在問：

- 需要幾次插入
- 幾次刪除
- 幾次替換
- 某些方法也考慮字元交換

如果資料中常見的是簡單 typo，這一類方法通常很有用。

## Finding the Closest Match with `amatch()`

當你有一個輸入值，想找它最像哪個候選字串時，可以用 `amatch()`：

```r
stringdist::amatch(
  x = "Sonday",
  table = c("Friday", "Saturday", "Sunday")
)
```

它的重點不是回傳所有距離，而是幫你選最接近的候選值。這很適合：

- 使用者輸入修正
- 類別標籤標準化
- 小型字典比對

## Q-grams and Token-Style Similarity

課程也介紹了 q-gram family，先把字串拆成固定長度片段，再比較重疊程度。

```r
stringdist::qgrams("Honolulu", "Hanolulu", q = 2)
```

相關方法包括：

- `qgram`
- `jaccard`
- `cosine`

```r
stringdist::stringdist(a, b, method = "qgram")
stringdist::stringdist(a, b, method = "jaccard")
stringdist::stringdist(a, b, method = "cosine")
```

這類方法比較不像「編輯幾步」，而是比較像「兩個字串由哪些片段組成、重疊多少」。

當字串較長，或你更在意局部片段相似性時，q-gram 類方法往往更合理。

## Choosing a Distance Is a Modeling Choice

不同方法反映不同假設：

- 若常見單字母 typo，先想 Levenshtein family
- 若在意局部片段重疊，先想 q-gram / cosine / jaccard
- 若資料很短，距離閾值通常要更保守

Key point: 沒有 universally best string distance。方法選擇其實是在選你認為「相似」應該如何被定義。

## Fuzzy Joins

當兩張表不能用完全相同的 key 直接 join 時，可以用 fuzzy join：

```r
fuzzyjoin::stringdist_join(
  user_input,
  database,
  by = "name"
)
```

這種 join 適合：

- 兩份來源對同一實體有不同拼法
- 名單清理與主檔對應
- 把人工輸入對回標準資料表

但要很小心：fuzzy join 很方便，也很容易把錯的東西 join 在一起。

## Custom Matching Rules

課程後面示範了把 string distance 和其他條件一起組合。

例如先定義一個可接受的小距離：

```r
small_str_distance <- function(left, right) {
  stringdist::stringdist(left, right) <= 5
}
```

然後再和其他數值條件一起放進 fuzzy join 邏輯。

這提醒一個很重要的實務觀念：

- 真正的 matching 很少只看一個欄位
- 名稱近似只是 evidence 之一
- 若能再加日期、數值、地區等條件，匹配會可靠很多

## `fuzzy_left_join()`

如果你要自己定義多欄匹配邏輯，可以考慮：

```r
fuzzyjoin::fuzzy_left_join(
  a, b,
  by = c(
    "name" = "name",
    "amount" = "amount"
  )
)
```

這類做法適合：

- 一欄用字串距離
- 一欄用數值容忍範圍
- 多欄共同決定同一筆 match

它通常比「單欄 stringdist 就直接 join」更接近真實資料整併需求。

## Regex vs Fuzzy Matching

兩者常一起出現在文字清理流程，但用途不同：

- regex：規則明確，回答「符合哪個模式」
- string distance：資料有誤差，回答「最接近哪個值」

實務上常見順序是：

1. 先用 regex / string cleaning 正規化格式
2. 再對剩下的不一致值做 fuzzy matching

如果原始字串中有多餘空白、標點、前後綴，先清理再算距離，通常會準很多。

## Practical Workflow

一個穩健的近似比對流程通常是：

1. 先把大小寫、空白、標點做基本標準化
2. 用 regex 或字串函數拆掉明顯噪音
3. 選定合適的 string distance method
4. 定義合理閾值，不要一開始就全自動接受 match
5. 對高風險結果保留人工審核或額外欄位驗證

## Common Mistakes

- 把 fuzzy matching 當成萬能清理工具，跳過前面的標準化。
- 距離閾值設太寬，導致錯誤 join。
- 只看名稱相似，不看其他欄位。
- 對不同長度、不同語言、不同資料來源的字串，卻用同一個閾值。

## Takeaways

- string distance 是量化「相似度」的一種方式，不是單純 pattern matching
- `stringdist()` 適合算距離，`amatch()` 適合找最近候選
- q-gram / jaccard / cosine 類方法更偏片段相似
- fuzzy join 很實用，但最好搭配多欄條件與人工 sanity check
- regex 與 fuzzy matching 常是前後相接的兩個步驟，不是互斥選項
