# Python Core Data Types

Python 的基礎資料結構很少，但幾乎所有資料處理、ETL、分析腳本都建立在它們上面。重點不是死背每個 method，而是知道什麼情境該選 `list`、`tuple`、`dict`、`set`，以及什麼時候該往 `collections` 模組找更適合的容器。

## 先抓住兩個軸

看資料型別時，先問兩件事：

- 資料有沒有順序？
- 資料會不會被修改？

一個很實用的簡化版心智模型：

- `list`：有順序、可修改
- `tuple`：有順序、不可修改
- `dict`：key-value 結構，依 key 取值
- `set`：不重複元素集合，適合做集合運算

## Interview Fast Comparison

如果面試官直接問「Python 主要資料結構差在哪」，最穩的回答順序通常是：

1. 先講順序與可變性
2. 再講典型操作
3. 最後講適用情境

可以很快收斂成：

- `list`: ordered, mutable, 適合反覆增刪改
- `tuple`: ordered, immutable, 適合固定結構資料
- `dict`: key-value mapping, 適合欄位查找
- `set`: unique elements, 適合 membership test 和集合運算

這種回答通常比一開始就背 methods 更有辨識度，因為它在回答「為什麼選這個容器」。

## Lists

`list` 是最常用的可變容器，適合放一批同類型資料，或一個需要反覆增刪改查的有序序列。

```python
cookies = ["chocolate chip", "brownie", "oreo"]

print(cookies[0])     # chocolate chip
print(cookies[-1])    # oreo
```

### 常見操作

```python
cookies = ["chocolate chip", "brownie"]
cookies.append("oreo")
cookies.extend(["peanut butter", "oatmeal raisin"])

removed = cookies.pop()
print(removed)  # oatmeal raisin
```

- `append()` 加一個元素
- `extend()` 合併另一個 iterable
- `pop()` 移除並回傳元素

### `+` and `list()` Do Different Jobs

list 初學時常有兩個很容易混淆的地方：

```python
fam = ["liz", 1.73, "emma", 1.68]
fam_ext = fam + ["me", 1.79]
fam_copy = list(fam)
```

- `fam + [...]` 是建立一個**內容更長**的新 list
- `list(fam)` 是建立一個**內容相同**的新 list

也就是說：

- `+` 比較像 concatenation
- `list(...)` 比較像 shallow copy

Key point: `list` 的 `+` 不是數值加法，而是把兩段序列接起來。

### 排序與搜尋

```python
scores = [5, 1, 9, 3]
print(sorted(scores))  # [1, 3, 5, 9]
print(9 in scores)     # True
```

如果你只是想保留原 list，不要直接用 `.sort()` 改原地資料；`sorted()` 比較安全。

### Interview Prompt: Why Choose `list`?

面試裡如果被追問為什麼用 `list`，重點通常不是「它最常見」，而是：

- 需要穩定順序
- 需要 index / slicing
- 需要 append / extend / pop 這類可變操作

如果題目主要在問 membership lookup 或 deduplication，答案往往就不該是 `list`。

## Tuples

`tuple` 適合表達「一筆固定結構資料」，或你想讓它不被不小心修改。

```python
point = (25.03, 121.56)
name, price = ("Anzac", 1.99)
```

### Zip 與 Unpack

tuple 很常在 `zip()` 和解包時自然出現。

```python
us_cookies = ["Chocolate Chip", "Brownies"]
in_cookies = ["Punjabi", "Fruit Cake Rusk"]

top_pairs = list(zip(us_cookies, in_cookies))
print(top_pairs)
# [('Chocolate Chip', 'Punjabi'), ('Brownies', 'Fruit Cake Rusk')]

for us_cookie, in_cookie in top_pairs:
    print(us_cookie, in_cookie)
```

### Enumerate

```python
for idx, item in enumerate(top_pairs):
    print(idx, item)
```

`enumerate()` 很適合在 loop 中同時拿索引與值，比手動維護 counter 乾淨很多。

### 易踩坑：單元素 tuple

```python
item = ("butter",)
print(type(item))  # <class 'tuple'>
```

關鍵不是括號，而是逗號。`("butter")` 仍然只是字串。

### Interview Prompt: Why Choose `tuple`?

`tuple` 最常被問的點不是語法，而是「為什麼不用 list」。

一個夠好的回答通常是：

- tuple 比較像 fixed record
- 不希望資料被意外修改
- 可以安全 unpack
- 很常自然出現在 `zip()`、multiple return values 和 dictionary keys 裡

## Strings

字串是不可變序列。很多資料清理工作的第一步，其實都是字串標準化。

### f-string

```python
cookie_name = "Anzac"
cookie_price = "$1.99"

print(f"Each {cookie_name} cookie costs {cookie_price}.")
```

### `join()`

```python
child_ages = ["3", "4", "7", "8"]
print(", ".join(child_ages))
```

`join()` 的心智模型是：分隔符字串主動把 iterable 黏起來。

### 常用清理動作

```python
name = "  Alice  "
print(name.strip().lower())
```

也很常搭配：

- `startswith()`
- `endswith()`
- `in`
- `replace()`

如果文字規則開始變複雜，再考慮用 regex，參考 [regex.md](regex.md)。

## Dictionaries

`dict` 適合描述具有欄位名稱的資料，或把 key 映射到 value。

```python
person = {
    "name": "Alice",
    "age": 30,
}

print(person["name"])  # Alice
```

### 安全取值

```python
print(person.get("email"))                # None
print(person.get("email", "not found"))   # not found
```

`dict[key]` 在 key 不存在時會直接噴 `KeyError`，`get()` 比較適合讀可能缺值的欄位。

### 更新資料

```python
person["city"] = "Taipei"
person.update({"age": 31, "role": "analyst"})
```

### Duplicate Keys: The Last Value Wins

```python
products = {"AG32": 10, "AG32": 20, "HT91": 30}
print(products["AG32"])  # 20
```

字典 key 必須唯一。如果同一個 key 在 literal 中重複出現，後面的值會覆蓋前面的值。

這在整理 mapping table 或手動建立設定字典時特別值得注意，因為 Python 不會主動警告你。

### 巢狀字典

```python
profile = {
    "user": {
        "name": "Alice",
        "contact": {"email": "a@example.com"},
    }
}

print(profile["user"]["contact"]["email"])
```

巢狀結構很常出現在 JSON 與 API 回應裡。

### Interview Prompt: Why Choose `dict`?

如果問題的核心是：

- 用名稱找值
- 建 mapping
- 組一筆有欄位的 record

`dict` 幾乎就是第一選擇。

面試時也很常被補問：

- key 必須唯一
- key 必須可 hash
- `get()` 比直接索引更適合讀可能缺值的欄位

## Sets

`set` 是不重複元素的集合，適合做去重與集合運算。

```python
cookies_eaten_today = [
    "chocolate chip",
    "oatmeal cream",
    "chocolate chip",
]

types_of_cookies_eaten = set(cookies_eaten_today)
print(types_of_cookies_eaten)
```

### 常見操作

```python
cookie_types = {"chocolate chip", "oatmeal cream"}
cookie_types.add("biscotti")
cookie_types.update(["anzac", "peanut butter"])
cookie_types.discard("biscotti")
```

- `add()` 加一個元素
- `update()` 合併另一個 set 或 iterable
- `discard()` 安全移除，不存在也不會報錯

### 集合運算

```python
cookies_jason_ate = {"chocolate chip", "oatmeal cream", "peanut butter"}
cookies_hugo_ate = {"chocolate chip", "anzac"}

print(cookies_jason_ate.union(cookies_hugo_ate))
print(cookies_jason_ate.intersection(cookies_hugo_ate))
print(cookies_jason_ate.difference(cookies_hugo_ate))
```

如果你在做名單比對、差集、交集，`set` 通常比 `list` 更自然也更快。

### Set Limitations

`set` 很快，但也有代價：

- 沒有穩定位置可言
- 不能用 index 取值
- 不能像 list 那樣直接 slice

```python
attendees = {"John", "Alan", "Roger"}

# attendees[0]  # TypeError: 'set' object is not subscriptable
```

如果你需要排序後查看內容，可以先轉成 list，或直接用 `sorted()`：

```python
ordered_attendees = sorted(attendees)
print(type(ordered_attendees))  # <class 'list'>
```

也就是說，`sorted(set_obj)` 的結果不是 set，而是 list。

### Interview Prompt: Why Choose `set`?

`set` 最常見的高分回答不是「它不能重複」，而是：

- membership test 很自然
- deduplication 很方便
- union / intersection / difference 直接對應題目語意

如果一個題目一直在做：

- `x in ...`
- 找交集
- 找差集

通常就是在暗示 `set`。

## Numeric Types

大部分時候你只會用到 `int` 和 `float`。

```python
big_int = 123456789123456789
approx_float = float(big_int)
```

要記得：

- `int` 可表達任意大的整數
- `float` 是近似值，不適合精確金額計算

### `Decimal`

```python
from decimal import Decimal

price = Decimal("19.99")
tax = Decimal("0.05")
total = price * (Decimal("1") + tax)
```

涉及金額、精確小數時，`Decimal` 通常比 `float` 更合適。

## `collections` 模組的高槓桿工具

當內建容器快不夠用時，先看 `collections`。

### `Counter`

`Counter` 是專門做頻率統計的字典。

```python
from collections import Counter

items = ["truck", "cart", "truck", "restaurant"]
counts = Counter(items)

print(counts["truck"])        # 2
print(counts.most_common(2))  # [('truck', 2), ('cart', 1)]
```

### `defaultdict`

`defaultdict` 能避免你每次都先判斷 key 是否存在。

```python
from collections import defaultdict

eateries_by_park = defaultdict(list)
eateries_by_park["M010"].append("Snack Bar")

contact_counts = defaultdict(int)
contact_counts["phones"] += 1
```

很適合：

- 分組收集 list
- 計數累加
- 建立巢狀結構

### `namedtuple`

`namedtuple` 是「有欄位名的 tuple」，適合表達輕量且不可變的記錄。

```python
from collections import namedtuple

Eatery = namedtuple("Eatery", ["name", "location", "park_id"])
eatery = Eatery("Snack Bar", "Central Park", "M010")

print(eatery.name)     # Snack Bar
print(eatery[0])       # Snack Bar
```

如果你只需要簡單欄位名稱、又不想上 class 或 dataclass，`namedtuple` 很夠用。

## 實務上的選擇直覺

- 一串可增刪改的資料：`list`
- 一筆固定結構記錄：`tuple`
- 欄位名稱對應值：`dict`
- 去重或集合運算：`set`
- 頻率統計：`Counter`
- 自動補預設值：`defaultdict`

## Summary

- 先從「有沒有順序」和「會不會修改」理解資料型別。
- `list`、`tuple`、`dict`、`set` 是 Python 最核心的容器。
- `zip()`、unpack、`enumerate()` 會讓 tuple 在實務上非常常見。
- `dict.get()`、`set` 集合運算、`Counter`、`defaultdict` 都是高頻率實戰工具。
- 需要精確小數時計算時，優先考慮 `Decimal`。
