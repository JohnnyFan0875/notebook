# Python Regular Expressions

當文字資料有固定但不完全規則的格式時，regex 很適合拿來做擷取、驗證、取代與切分。它最有價值的場景通常不是「所有字串都用 regex 解」，而是當一般 `split()`、`replace()`、`in` 已經不足以描述模式時，再用 regex 精準表達規則。

## 先有一個心智模型

regex 本質上是在描述一種文字模式：

- 哪些字元可以出現
- 可以出現幾次
- 必須出現在什麼位置
- 哪一段要被擷取出來

Python 主要透過 `re` 模組使用 regex：

```python
import re
```

## 為什麼常寫 raw string

大多數 regex 都建議寫成 raw string，也就是 `r"..."`。

```python
pattern = r"\d+"
```

因為反斜線 `\` 在 Python 字串與 regex 裡都有特殊意義。用 raw string 可以少掉很多雙重 escaping 的困擾。

## 最常用的函式

### `re.search()`

找整個字串中第一個符合的位置。

```python
match = re.search(r"\d+", "Order number: 48291")
print(match.group())  # 48291
```

### `re.match()`

只從字串開頭開始比。

```python
print(re.match(r"\d+", "123abc").group())  # 123
print(re.match(r"\d+", "abc123"))          # None
```

如果你是想檢查「是不是出現在任意位置」，通常要用 `re.search()`，不是 `re.match()`。

### `re.findall()`

把所有符合的結果收集成 list。

```python
print(re.findall(r"\d+", "I saw 3 cats and 14 dogs"))
# ['3', '14']
```

### `re.sub()`

用規則取代文字。

```python
text = "Call me at 02-123-4567"
cleaned = re.sub(r"\d", "X", text)
print(cleaned)  # Call me at XX-XXX-XXXX
```

### `re.split()`

用 pattern 當作切分規則。

```python
text = "one. two. three"
print(re.split(r"\.\s*", text))
# ['one', 'two', 'three']
```

## 基本符號

### Character Classes

- `\d`：數字
- `\w`：英數字與底線
- `\s`：空白
- `\D`、`\W`、`\S`：對應的反集合

```python
re.findall(r"User\w", "The winners are: User9, UserN, User8")
# ['User9', 'UserN', 'User8']
```

也可以自己定義字元集合：

```python
re.findall(r"[A-Za-z]+\d", "roomA2 roomB7")
# ['roomA2', 'roomB7']
```

排除集合則用 `[^...]`：

```python
re.findall(r"www[^0-9]+com", "www.example.com www3example.com")
# ['www.example.com']
```

### Quantifiers

- `+`：1 次以上
- `*`：0 次以上
- `?`：0 或 1 次
- `{m}`：剛好 m 次
- `{m,n}`：m 到 n 次

```python
re.findall(r"colou?r", "color colour")
# ['color', 'colour']

re.search(r"\w{8}\d{4}", "passwordABCD1234")
```

### Anchors

- `^`：字串開頭
- `$`：字串結尾

```python
re.findall(r"^the\s\d+s", "the 3s are here")
re.findall(r"the\s\d+s$", "we only keep the 3s")
```

如果 pattern 應該匹配整個欄位，而不是欄位中的一小段，anchor 常常是必要的。

## Grouping 與 Capturing

括號 `(...)` 有兩個角色：

- 把一段 pattern 視為同一組
- 把符合內容擷取出來

```python
text = "Clary has 2 friends, Susan has 3 brothers"

print(re.findall(r"([A-Za-z]+)\s\w+\s(\d+)\s(\w+)", text))
# [('Clary', '2', 'friends'), ('Susan', '3', 'brothers')]
```

這在做結構化抽取時非常好用。

### `group()` 讀取 Match Object

```python
text = "The date is 12-05-2024."
info = re.search(r"(\d{1,2})-(\d{2})-(\d{4})", text)

print(info.group(0))  # 12-05-2024
print(info.group(3))  # 2024
```

- `group(0)` 是整個 match
- `group(1)`、`group(2)`... 是各 capturing group

### Non-capturing Group

有時你只是想分組，不想把它變成輸出欄位，就用 `(?:...)`。

```python
text = "Today is 21st and tomorrow is 22nd"
print(re.findall(r"(\d+)(?:st|nd|rd|th)", text))
# ['21', '22']
```

這在 alternation 很常用，能避免 `findall()` 回傳一堆你其實不想要的中間群組。

## Alternation

`|` 表示「或」。

```python
re.findall(r"cat|dog|bird", "I saw a dog and a bird")
# ['dog', 'bird']
```

但 alternation 跟 grouping 常常要一起用，不然優先順序容易誤判：

```python
re.findall(r"\d+\s(cat|dog|bird)", "1 cat 2 dog 3 bird")
# ['cat', 'dog', 'bird']
```

## Named Groups

當 group 變多時，用名字會比靠編號更可讀。

```python
text = "Seattle zip 98101"
match = re.search(r"(?P<city>[A-Za-z]+).*?(?P<zipcode>\d{5})", text)

print(match.group("city"))     # Seattle
print(match.group("zipcode"))  # 98101
```

這對長 pattern 或 ETL 抽欄位特別有幫助。

## Backreference

backreference 可以重用前面已經捕捉到的內容，適合抓重複字、重複代碼等問題。

```python
sentence = "go go stop"
print(re.findall(r"(\w+)\s\1", sentence))
# ['go']

print(re.sub(r"(\w+)\s\1", r"\1", sentence))
# go stop
```

named group 也可以做 backreference：

```python
sentence = "code 12345 and code 12345"
print(re.findall(r"(?P<code>\d{5}).*?(?P=code)", sentence))
# ['12345']
```

## Greedy vs Non-greedy

預設 quantifier 多半是 greedy，也就是「盡可能多吃」。

```python
re.findall(r"www.+com", "www.example.com and www.test.com")
# 可能吃到比你想像更長的一段
```

加上 `?` 會改成 non-greedy：

```python
re.match(r".*?hello", "xhelloxxxxxx").group()
# xhello
```

這在 HTML、URL、括號內容等模式上很常遇到。

## Regex 很適合的實務場景

- 從文字中抽電話、日期、郵遞區號、帳號片段
- 找出 user handle、email-like token、hashtag
- 清掉特殊符號或重複空白
- 驗證欄位格式是否大致合理

例如抽電話：

```python
phone_number = "My number is 1-234-567-8910"
re.findall(r"\d{1,2}-\d{3}-\d{2,3}-\d{4,}", phone_number)
# ['1-234-567-8910']
```

## 什麼時候不要急著用 Regex

- 只是固定字串替換：先用 `replace()`
- 只是簡單前後綴檢查：先用 `startswith()` / `endswith()`
- 已經有結構化格式：先用專門 parser，例如 URL、JSON、HTML parser

regex 很強，但也很容易把簡單問題寫得難維護。

## Summary

- `re.search()` 找任意位置第一個 match。
- `re.match()` 只看開頭。
- `re.findall()` 適合批次擷取，`re.sub()` 適合清理，`re.split()` 適合規則切分。
- `()`, `(?:...)`, `(?P<name>...)` 分別對應 capturing、non-capturing、named group。
- backreference 能抓重複模式。
- greedy / non-greedy 差異常是 regex bug 的來源。
