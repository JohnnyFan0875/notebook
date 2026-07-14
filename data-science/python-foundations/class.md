# Python Classes

## Defining a Class

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

# Usage
p = Person("Alice", 30)
print(p.greet())
```

- `__init__` → constructor method that initializes object attributes.
- `self` → reference to the instance itself.

## Instance Attributes vs Class Attributes

```python
class Dog:
    species = "Canis familiaris"  # Class attribute (shared by all instances)

    def __init__(self, name):
        self.name = name          # Instance attribute (unique per instance)

fido = Dog("Fido")
rex = Dog("Rex")

print(fido.species)  # "Canis familiaris"
print(rex.name)      # "Rex"
```

## Instance Methods, Class Methods, Static Methods

```python
class MyClass:
    def instance_method(self):
        return "This is an instance method", self

    @classmethod
    def class_method(cls):
        return "This is a class method", cls

    @staticmethod
    def static_method():
        return "This is a static method"

obj = MyClass()
print(obj.instance_method())
print(MyClass.class_method())
print(MyClass.static_method())
```

- **Instance methods** → operate on object (`self`).
- **Class methods** → operate on the class itself (`cls`).
- **Static methods** → independent, don’t use `self` or `cls`.

## Class Attribute Pitfall

class attribute 很適合放 shared constants，但要注意 instance assignment 可能只是在該物件上建立同名 instance attribute。

```python
class Employee:
    MIN_SALARY = 30000

    def __init__(self, name, salary):
        self.name = name
        self.salary = max(salary, Employee.MIN_SALARY)

emp = Employee("John", 25000)
print(emp.salary)        # 30000
print(emp.MIN_SALARY)    # 30000

emp.MIN_SALARY = 10000
print(emp.MIN_SALARY)         # 10000  (instance attribute)
print(Employee.MIN_SALARY)    # 30000  (class attribute unchanged)
```

- 讀取時 Python 會先找 instance，再找 class。
- 對 `emp.MIN_SALARY = ...` 賦值，不會改到 `Employee.MIN_SALARY` 本身。
- 如果這個值真的屬於整個 class，通常應該透過 `Employee.MIN_SALARY` 修改。

## Alternative Constructors with `@classmethod`

Python 只有一個 `__init__()`，所以如果你想提供不同建構入口，常見做法是用 classmethod。

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @classmethod
    def from_string(cls, text):
        name, salary = text.split(",")
        return cls(name, int(salary))

emp = Employee.from_string("Alice,50000")
print(emp.name, emp.salary)  # Alice 50000
```

- `cls(...)` 會呼叫該 class 的 constructor。
- 這很適合處理來自 CSV、env vars、config strings 等替代輸入格式。
- 與其手動堆很多 if/else 在 `__init__()`，通常用 classmethod 會更清楚。

## Calling Parent Logic with `super()`

在繼承中，如果 child class 需要延用 parent 的初始化或方法，通常優先用 `super()`，而不是直接寫 parent class 名稱。

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(Person):
    def __init__(self, name, age, title):
        super().__init__(name, age)
        self.title = title
```

- `super().__init__(...)` 不需要手動傳 `self`
- 它比 `Person.__init__(self, ...)` 更容易維護
- 當 class hierarchy 變複雜，特別是多重繼承時，`super()` 才能配合 Python 的 method resolution order 正常工作

如果你直接把 parent class 名稱寫死，後續重構繼承關係時比較容易出錯。

## Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..." # This prevents errors if .speak() is called on an Animal that doesn’t override it.

class Cat(Animal):
    def speak(self):
        return "Meow"

class Dog(Animal):
    def speak(self):
        return "Woof"

animals = [Cat("Kitty"), Dog("Fido")]
for a in animals:
    print(f"{a.name} says {a.speak()}")
```

- Child classes override methods of parent classes.
- Enables polymorphism (different behavior depending on object type).

## Multiple Inheritance and MRO

Python 支援多重繼承，但要保守使用。它最容易讓人混亂的地方，不是語法，而是「同名方法最後到底會走哪一個 class」。

```python
class Employee:
    def role(self):
        return "employee"

class Student:
    def role(self):
        return "student"

class Intern(Employee, Student):
    pass

print(Intern.mro())
print(Intern().role())
```

這裡的搜尋順序遵守 MRO, method resolution order。

- child class 先找
- 再依照 parent classes 在 class 定義中出現的順序，由左到右找
- 可以用 `ClassName.mro()` 或 `ClassName.__mro__` 檢查實際順序

`class Intern(Employee, Student)` 和 `class Intern(Student, Employee)` 的結果可能不同，所以多重繼承不是只有「拿到兩邊功能」這麼簡單。

實務上如果只是想重用功能，通常先問自己：

- 這是不是比較適合 composition
- 這個共用行為是否能抽成 helper object

如果真的要用多重繼承，`super()` 幾乎是必要工具。

## Encapsulation (Private Attributes)

Unlike Java or C++, Python has no true private keyword. All attributes are accessible if you really want to get them. Instead, Python relies on naming conventions to signal the intent of the programmer.

```python
class Account:
    def __init__(self, balance):
        self._balance = balance   # Protected (convention)
        self.__secret = 1234      # Name mangling: _Account__secret

    def deposit(self, amount):
        self._balance += amount
        return self._balance
```

- `_attr` → protected by convention (internal use). Tools like linters and IDEs may warn if you access it directly.
- `__attr` → triggers name mangling (`_ClassName__attr`). This prevents accidental access from subclasses or external code. Not truly private — just harder to access by mistake.

## Properties (Getters and Setters)

```python
class Celsius:
    def __init__(self, temperature=0):
        self._temperature = temperature

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible")
        self._temperature = value

c = Celsius()
c.temperature = 25
print(c.temperature)
```

- `@property` → getter.
- `@<name>.setter` → setter with validation.

`@property` 背後其實是 descriptor protocol 的較高階介面，所以它不只是「把 method 偽裝成 attribute」，也可以控制讀取、賦值、刪除時的行為。

```python
class Student:
    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn

    @property
    def ssn(self):
        return "XXX-XX-" + self._ssn[-4:]

    @ssn.setter
    def ssn(self, new_ssn):
        self._ssn = new_ssn

    @ssn.deleter
    def ssn(self):
        raise AttributeError("Can't delete SSN")
```

這種模式很適合：

- 需要遮罩敏感資訊
- 需要在賦值時驗證資料
- 想保留舊 API 形式，但逐步把內部實作改掉

重點是對外仍然看起來像 `obj.ssn`，而不是 `obj.get_ssn()`。

## Abstract Base Classes

當你不是只想「提供預設實作」，而是想明確宣告「子類別必須實作哪些方法」，可以用 abstract base class, ABC。

```python
from abc import ABC, abstractmethod

class School(ABC):
    @abstractmethod
    def enroll(self):
        pass

    def graduate(self):
        print("Congrats on graduating!")
```

重點：

- abstract method 定義的是 contract
- 繼承者如果沒有實作所有 abstract methods，就不能被實例化
- ABC 可以同時包含 abstract methods 與 concrete methods

這很適合用在 framework、plugin system、或多個 subclass 必須遵守同一份介面的情境。

## Magic Methods

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
```

- `__repr__` → string representation.
- `__add__`, `__sub__`, etc. → operator overloading.

### Object Equality and `__eq__`

很多初學者第一次踩到的坑是：兩個看起來資料完全一樣的物件，`==` 竟然還是 `False`。

```python
class Customer:
    def __init__(self, name, balance, customer_id):
        self.name = name
        self.balance = balance
        self.customer_id = customer_id

customer1 = Customer("Maryam Azar", 3000, 123)
customer2 = Customer("Maryam Azar", 3000, 123)

print(customer1 == customer2)  # False
```

原因不是資料不同，而是預設情況下，使用者自訂 class 的相等比較常接近「是不是同一個物件 reference」。

如果你想表達的是「只要關鍵欄位相同，就視為相等」，就要自己定義 `__eq__`：

```python
class Customer:
    def __init__(self, name, balance, customer_id):
        self.name = name
        self.balance = balance
        self.customer_id = customer_id

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return self.customer_id == other.customer_id
```

幾個實務提醒：

- `a is b` 問的是兩個變數是否指向同一個物件
- `a == b` 問的是兩個物件在你定義的語意下是否相等
- 若 class 是 mutable，定義 `__eq__` 之後通常也要更小心 hash 與 dict/set 行為

### Polymorphism Means "Program to the Interface"

多型最有用的地方，不是名詞定義，而是它讓呼叫端不需要到處寫型別判斷。

```python
class BankAccount:
    def withdraw(self, amount):
        self.balance -= amount

class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        self.balance -= amount + 1

class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        self.balance -= amount

def batch_withdraw(accounts, amount):
    for account in accounts:
        account.withdraw(amount)
```

`batch_withdraw()` 不需要問「這是不是 `CheckingAccount`」，只需要相信每個物件都提供 `withdraw()` 這個介面。

這個思路比到處寫：

```python
if isinstance(account, CheckingAccount):
    ...
elif isinstance(account, SavingsAccount):
    ...
```

更容易維護。當新 class 加進來時，只要遵守同一個介面，呼叫端通常不用改。

## Best Practices

- Use classes for grouping related data and behavior.
- Keep methods small and focused.
- Prefer composition over deep inheritance.
- Prefer `super()` over hard-coding parent class names.
- Use ABCs when you need a contract, not just shared code.
- Use `@property` for controlled attribute access.
- Document classes with docstrings.

## Summary

- Classes define blueprints for objects.
- Use `__init__` to set up instances.
- Attributes can be instance-specific or shared at class-level.
- Methods can be instance, class, or static.
- Inheritance and polymorphism allow code reuse and flexibility.
- Magic methods provide custom behavior for built-in operators.
