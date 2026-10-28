[Data Science](../README.md) › [Python Foundations](README.md) › 類別

# 類別與物件導向 (Classes & OOP)

class 把相關的資料（屬性）與行為（方法）綁在一起。資料分析程式常用到的是：`dataclass` 表達記錄、`@property` 做驗證、繼承 / ABC 定義共同介面（例如 sklearn 的 `fit` / `transform`）。

## 定義與屬性

```python
class Sample:
    assay = "RNA-seq"                     # 類別屬性：所有實例共用

    def __init__(self, sample_id, condition):
        self.sample_id = sample_id        # 實例屬性：每個物件各自一份
        self.condition = condition

    def __repr__(self):                   # 給開發者看的表示法（互動環境、除錯）
        return f"Sample({self.sample_id!r}, {self.condition!r})"

    def label(self):
        return f"{self.sample_id}_{self.condition}"

s = Sample("S1", "treated")
s.label()                                 # 'S1_treated'
```

`__init__` 是初始化方法，`self` 指向實例本身。

### 陷阱：類別屬性被同名實例屬性遮蔽

```python
class Employee:
    MIN_SALARY = 30000
    def __init__(self, salary):
        self.salary = max(salary, Employee.MIN_SALARY)

emp = Employee(25000)
emp.salary                                # 30000
emp.MIN_SALARY = 10000                    # 只在 emp 上建立同名實例屬性
Employee.MIN_SALARY                       # 30000：類別屬性沒變

class Bad:
    items = []                            # 可變的類別屬性：所有實例共用同一個 list！
```

讀取時先找實例、再找類別；賦值永遠寫在實例上。要改共用值就寫 `Employee.MIN_SALARY = ...`；可變的預設值放在 `__init__` 裡建立。

## 三種方法

| 方法 | 第一個參數 | 用途 |
| --- | --- | --- |
| 實例方法 | `self` | 操作某個物件的資料（最常見） |
| `@classmethod` | `cls` | 替代建構子 (alternative constructor)、操作類別層級狀態 |
| `@staticmethod` | 無 | 和類別相關但不需要實例或類別狀態的工具函式 |

```python
class Employee:
    def __init__(self, name, salary):
        self.name, self.salary = name, salary

    @classmethod
    def from_string(cls, text):           # 從 CSV 行、設定字串等其他格式建立物件
        name, salary = text.split(",")
        return cls(name, int(salary))     # 用 cls 而非寫死類別名，子類別繼承後也正確

    @staticmethod
    def is_valid_salary(x):
        return x > 0

Employee.from_string("Alice,50000").salary  # 50000
```

Python 只有一個 `__init__`；需要多種建構方式時用 classmethod，不要在 `__init__` 裡堆 if/else（pandas 的 `pd.DataFrame.from_dict` 就是這個模式）。

## `dataclass`：記錄型類別首選

只是要存幾個欄位時，`dataclass` 自動產生 `__init__`、`__repr__`、`__eq__`。

```python
from dataclasses import dataclass, field

@dataclass
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    filters: list[str] = field(default_factory=list)   # 可變預設值要用 default_factory

    def is_snv(self) -> bool:
        return len(self.ref) == len(self.alt) == 1

v = Variant("chr17", 7675088, "C", "T")
v                                         # Variant(chrom='chr17', pos=7675088, ref='C', alt='T', filters=[])
v == Variant("chr17", 7675088, "C", "T")  # True：依欄位比較

@dataclass(frozen=True)                   # 不可變，且可 hash → 能當 dict key / 放進 set
class Locus:
    chrom: str
    pos: int
```

| 選擇 | 何時用 |
| --- | --- |
| `dict` | 欄位不固定、來自 JSON |
| `namedtuple` | 不可變、輕量、需要 tuple 行為 |
| `dataclass` | 固定欄位 + 型別註記 + 可能有方法（多數情況） |
| 一般 class | 有複雜狀態與行為 |
| `pydantic` 模型 | 需要執行期型別驗證（API、設定檔） |

## 繼承與 `super()`

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)            # 沿用父類別初始化；不必傳 self
        self.breed = breed
    def speak(self):                      # 覆寫 (override)
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

[f"{a.name}: {a.speak()}" for a in [Dog("Fido", "lab"), Cat("Kitty")]]   # 多型
```

用 `super()` 而不寫死 `Animal.__init__(self, ...)`：重構繼承關係時不易出錯，也是多重繼承下依 MRO 正確串接的前提。

### 多重繼承與 MRO

```python
class Employee:
    def role(self): return "employee"
class Student:
    def role(self): return "student"
class Intern(Employee, Student):
    pass

Intern().role()                           # 'employee'：依 MRO 由左到右找
Intern.mro()                              # [Intern, Employee, Student, object]
```

方法解析順序 (MRO, method resolution order)：先找子類別，再依定義時父類別的順序由左到右。只是想重用功能時，先考慮**組合 (composition)**：把共用行為抽成另一個物件當屬性，而不是加深繼承。

## 多型：對介面寫程式 (Program to the Interface)

```python
def batch_withdraw(accounts, amount):
    for account in accounts:
        account.withdraw(amount)          # 不問型別，只要求有 withdraw()
```

呼叫端不寫 `if isinstance(...)` 分支；新類別只要提供同樣的方法就能直接用。這就是 duck typing，也是 sklearn 能把任何有 `fit` / `predict` 的物件放進 `Pipeline` 的原因。

## 抽象基底類別 (Abstract Base Class)

要**強制**子類別實作某些方法時用 ABC。

```python
from abc import ABC, abstractmethod

class Normalizer(ABC):
    @abstractmethod
    def transform(self, counts): ...      # 契約：子類別一定要實作

    def fit_transform(self, counts):      # ABC 也可以有具體方法
        return self.transform(counts)

class CPM(Normalizer):
    def transform(self, counts):
        total = sum(counts)
        return [c / total * 1e6 for c in counts]

# Normalizer()                            # TypeError：沒實作抽象方法不能實例化
```

## 封裝與 `@property`

Python 沒有真正的 private，靠命名慣例：

| 命名 | 意義 |
| --- | --- |
| `attr` | 公開 |
| `_attr` | 內部使用（慣例），linter / IDE 會提醒 |
| `__attr` | name mangling 成 `_ClassName__attr`，避免子類別意外覆蓋；不是真的私有 |

```python
class Celsius:
    def __init__(self, temperature=0):
        self.temperature = temperature    # 經過 setter，初始化時也會驗證

    @property
    def temperature(self):                # getter：外部仍寫 c.temperature
        return self._temperature

    @temperature.setter
    def temperature(self, value):         # setter：賦值時驗證
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._temperature = value

    @property
    def fahrenheit(self):                 # 唯讀的衍生屬性
        return self._temperature * 9 / 5 + 32

c = Celsius(25)
c.fahrenheit                              # 77.0
```

property 適合：賦值時驗證、遮罩敏感欄位（只顯示末 4 碼）、保留舊 API 形式但更換內部實作。

## 特殊方法 (Magic / Dunder Methods)

| 方法 | 觸發 | 用途 |
| --- | --- | --- |
| `__repr__` / `__str__` | `repr(x)` / `print(x)` | 開發者 / 使用者看的字串 |
| `__eq__` / `__hash__` | `==` / 放進 set、當 dict key | 自訂相等與雜湊 |
| `__lt__` 等 | `<`、`sorted()` | 排序（可用 `functools.total_ordering` 補齊） |
| `__add__` 等 | `+`、`-`… | 運算子多載 |
| `__len__`、`__getitem__`、`__iter__` | `len()`、`x[i]`、`for` | 讓物件像容器 |
| `__enter__` / `__exit__` | `with` | context manager |
| `__call__` | `x()` | 讓物件可呼叫 |

```python
class Customer:
    def __init__(self, name, customer_id):
        self.name, self.customer_id = name, customer_id

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented         # 交給另一邊處理，不要直接回 False
        return self.customer_id == other.customer_id

    def __hash__(self):                   # 定義 __eq__ 後 __hash__ 會被設為 None，要自己補
        return hash(self.customer_id)

a, b = Customer("Maryam", 123), Customer("Maryam", 123)
a == b                                    # True（沒定義 __eq__ 時是 False：預設比的是 identity）
a is b                                    # False：不是同一個物件
```

> `is` 問「是不是同一個物件」，`==` 問「在你定義的語意下是否相等」。可變物件若參與 hash，修改欄位後在 set / dict 裡會找不到。

## 設計原則

| 原則 | 說明 |
| --- | --- |
| 先問需不需要 class | 只是一組函式 → 模組；只是欄位 → `dataclass` |
| 組合優於深層繼承 | 繼承超過兩層就要重新考慮 |
| 方法小而專一 | 一個方法做一件事，方便測試（見 [測試](testing.md)） |
| 驗證放在邊界 | 在 `__init__` / setter 擋掉不合法狀態，不要讓壞物件存在 |
