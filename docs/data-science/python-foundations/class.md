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

## Best Practices

- Use classes for grouping related data and behavior.
- Keep methods small and focused.
- Prefer composition over deep inheritance.
- Use `@property` for controlled attribute access.
- Document classes with docstrings.

## Summary

- Classes define blueprints for objects.
- Use `__init__` to set up instances.
- Attributes can be instance-specific or shared at class-level.
- Methods can be instance, class, or static.
- Inheritance and polymorphism allow code reuse and flexibility.
- Magic methods provide custom behavior for built-in operators.
