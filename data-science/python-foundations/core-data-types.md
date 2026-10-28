[Data Science](../README.md) › [Python Foundations](README.md) › 核心資料型別

# 核心資料型別 (Core Data Types)

Python 內建容器只有幾種，但幾乎所有資料處理腳本都建立在它們上面。重點是知道什麼情境該選哪個容器，以及什麼時候改用 `collections`。

## 先看兩個軸：順序與可變性

| 型別 | 有序？ | 可變？ | 重複？ | 取值方式 | 典型用途 |
| --- | --- | --- | --- | --- | --- |
| `list` | 是 | 是 | 可 | index / slice | 一串會增刪改的資料 |
| `tuple` | 是 | 否 | 可 | index / unpack | 固定結構的一筆記錄、多重回傳值、dict key |
| `dict` | 插入順序（3.7+） | 是 | key 唯一 | key | 欄位名 → 值、mapping、JSON |
| `set` | 否 | 是 | 不可 | 只能 `in` / 迭代 | 去重、membership test、集合運算 |
| `str` | 是 | 否 | 可 | index / slice | 文字（不可變序列） |

| 操作 | `list` | `set` / `dict` |
| --- | --- | --- |
| `x in container` | O(n)，逐一比對 | 平均 O(1)，hash 查找 |
| 依位置取值 | O(1) | 不支援（set）/ 用 key（dict） |

> 若題目一直在做 `x in ...`、交集、差集（例如比對兩份基因 ID 清單），就該用 `set`，不是 `list`。

## List

```python
genes = ["TP53", "BRCA1"]
genes[0], genes[-1]                   # 'TP53', 'BRCA1'
genes.append("EGFR")                  # 加一個元素
genes.extend(["MYC", "KRAS"])         # 合併另一個 iterable
last = genes.pop()                    # 移除並回傳最後一個：'KRAS'

longer = genes + ["PTEN"]             # + 是串接，產生新 list
copy_ = list(genes)                   # 淺複製（shallow copy），等同 genes.copy() / genes[:]

sorted(genes)                         # 回傳新 list，不改原資料
genes.sort()                          # 原地排序，回傳 None
```

### 別名與淺複製 (Aliasing & Shallow Copy)

| 寫法 | 結果 |
| --- | --- |
| `b = a` | 同一個物件，改 `b` 就是改 `a` |
| `b = a.copy()` / `list(a)` | 新的外層 list，但**內層物件仍共用** |
| `b = copy.deepcopy(a)` | 連巢狀物件都複製 |

```python
import copy

a = [[1, 2], [3, 4]]
b = a.copy()
b[0].append(99)
a                       # [[1, 2, 99], [3, 4]]  內層被一起改到
c = copy.deepcopy(a)    # 完全獨立
grid = [[0] * 3] * 2    # 陷阱：兩列是同一個 list；改用 [[0] * 3 for _ in range(2)]
```

這和 pandas 的 view vs copy 是同一類問題，見 [pandas](pandas/README.md)。

## Tuple

```python
point = (25.03, 121.56)
chrom, pos = ("chr17", 7_675_088)     # 解包 (unpacking)
first, *rest = (1, 2, 3, 4)           # first=1, rest=[2, 3, 4]

pairs = list(zip(["A", "B"], [1, 2])) # [('A', 1), ('B', 2)]
for i, (name, n) in enumerate(pairs): # 同時取索引與值
    ...

single = ("butter",)                  # 單元素 tuple 靠逗號；("butter") 只是 str
```

選 `tuple` 而不選 `list` 的理由：表達固定結構的記錄、不希望被意外修改、可當 dict key（只要內容都可 hash）。

## String

字串不可變；大部分清理動作都會回傳新字串。

```python
name = "  Alice  "
name.strip().lower()                  # 'alice'
f"{name.strip()} scored {0.8765:.2f}" # f-string 格式化：'Alice scored 0.88'
", ".join(["3", "4", "7"])            # '3, 4, 7'：分隔符把 iterable 黏起來
"sample_01.fastq".endswith(".fastq")  # True
"ATGC".replace("T", "U")              # 'AUGC'
```

規則變複雜時改用 regex，見 [文字清理與正規表示式](text-cleaning-and-regex.md)。

## Dict

```python
person = {"name": "Alice", "age": 30}
person["name"]                        # 'Alice'
person.get("email")                   # None：key 不存在不會報錯
person.get("email", "not found")      # 指定預設值
person["city"] = "Taipei"             # 新增 / 覆寫
person.update({"age": 31, "role": "analyst"})
person | {"age": 32}                  # 3.9+：合併成新 dict，右邊優先

for key, value in person.items():
    ...

{"AG32": 10, "AG32": 20}["AG32"]      # 20：literal 裡重複的 key，後者覆蓋前者且不警告

profile = {"user": {"contact": {"email": "a@example.com"}}}
profile["user"]["contact"]["email"]   # 巢狀結構常見於 JSON / API 回應
```

- `dict[key]` 遇到不存在的 key 會丟 `KeyError`；讀可能缺值的欄位用 `get()`。
- key 必須可 hash：`str`、`int`、`tuple` 可以，`list`、`dict` 不行。

## Set

```python
s = set(["chr1", "chr2", "chr1"])     # {'chr1', 'chr2'}：去重
s.add("chrX")
s.update(["chr3", "chr4"])
s.discard("chr9")                     # 不存在也不報錯；remove() 會報 KeyError

a = {"TP53", "BRCA1", "EGFR"}
b = {"TP53", "MYC"}
a | b                                 # 聯集 union
a & b                                 # 交集 intersection：{'TP53'}
a - b                                 # 差集 difference：{'BRCA1', 'EGFR'}
a ^ b                                 # 對稱差：只出現在其中一邊

# s[0]                                # TypeError：set 不能用 index
sorted(s)                             # 要看排序結果先轉，回傳的是 list
```

> set 的迭代順序不保證，不要依賴它產生輸出順序；寫檔或比對前先 `sorted()`，結果才可重現。

## 數值型別 (Numeric Types)

| 型別 | 特性 | 用途 |
| --- | --- | --- |
| `int` | 任意精度，不會溢位 | 計數、索引、基因座位置 |
| `float` | IEEE 754 雙精度，**近似值** | 一般科學計算 |
| `Decimal` | 十進位精確小數 | 金額、需要精確小數的計算 |

```python
0.1 + 0.2 == 0.3                      # False：浮點誤差
import math
math.isclose(0.1 + 0.2, 0.3)          # True：比較浮點數用容差（numpy 用 np.isclose / np.allclose）

from decimal import Decimal
Decimal("19.99") * Decimal("1.05")    # Decimal('20.9895')；要從字串建，Decimal(19.99) 會帶入誤差
```

## `collections`：內建容器不夠用時

| 工具 | 用途 | 例子 |
| --- | --- | --- |
| `Counter` | 頻率統計 | k-mer、類別計數 |
| `defaultdict` | 自動補預設值，免判斷 key 是否存在 | 分組收集、累加 |
| `namedtuple` | 有欄位名的不可變記錄 | 輕量資料列（可變或需型別註記改用 `dataclass`，見 [類別](class.md)） |
| `deque` | 兩端 O(1) 增刪 | 佇列、滑動視窗 |

```python
from collections import Counter, defaultdict, namedtuple, deque

seq = "ATGCGATACGCTTGA"
kmers = Counter(seq[i:i + 3] for i in range(len(seq) - 2))
kmers.most_common(2)                  # 出現最多的兩個 3-mer

by_chrom = defaultdict(list)
for chrom, pos in [("chr1", 100), ("chr2", 50), ("chr1", 300)]:
    by_chrom[chrom].append(pos)       # {'chr1': [100, 300], 'chr2': [50]}

Variant = namedtuple("Variant", ["chrom", "pos", "ref", "alt"])
v = Variant("chr17", 7675088, "C", "T")
v.pos, v[0]                           # 7675088, 'chr17'

window = deque(maxlen=3)              # 只保留最近 3 個元素
```

## 選擇速查

| 需求 | 用 |
| --- | --- |
| 一串會增刪改、需要順序 / index | `list` |
| 一筆固定結構記錄、多重回傳值 | `tuple` / `namedtuple` |
| 欄位名對應值、查表 | `dict` |
| 去重、membership、集合比對 | `set` |
| 計數 | `Counter` |
| 分組收集 | `defaultdict(list)` |
| 大量同型別數值運算 | NumPy array（見 [NumPy](numpy/README.md)） |
