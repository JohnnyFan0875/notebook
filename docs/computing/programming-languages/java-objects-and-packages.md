# Java Objects and Packages

Once basic syntax and primitives are familiar, the next jump in Java is understanding how the language models data as objects and how code is organized into packages. This is where Java starts to feel less like a calculator language and more like an application language.

## Primitive Types vs Reference Types

Java types fall into two broad categories:

| Category | Examples |
| -------- | -------- |
| Primitive types | `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean` |
| Reference types | classes, interfaces, enums, arrays |

Primitive values are built into the language. Reference types point to objects or other structured values.

Key point: `String` is not a primitive, even though beginners often encounter it as early as primitives.

## POJOs

`POJO` stands for `Plain Old Java Object`. The core idea is simple: a class whose job is mainly to hold and move data, not to carry heavy framework coupling or business logic.

A useful mental model is:

- custom class defines the shape
- fields store the data
- getters and setters expose controlled access

## Typical POJO Structure

```java
public class Car {
    private String model;
    private int year;

    public Car() {
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }
}
```

## Common POJO Guidelines

Typical POJO conventions are:

- class is `public`
- fields are `private`
- access happens through public getters and setters
- a no-argument constructor is often provided
- the object stays focused on representing data

These are conventions, not laws, but they explain a lot of ordinary Java application code.

## Getters and Setters

Getters and setters are the standard naming convention for field access.

```java
public String getMake() {
    return make;
}

public void setMake(String make) {
    this.make = make;
}
```

Naming pattern:

- getter: `getFieldName()`
- boolean getter: often `isFieldName()`
- setter: `setFieldName(value)`

Key point: even if the method body is trivial, the method boundary still matters because it preserves encapsulation and gives you a place to add validation later.

## Wrapper Classes

Every primitive type has a corresponding wrapper class.

| Primitive | Wrapper |
| --------- | ------- |
| `byte` | `Byte` |
| `short` | `Short` |
| `int` | `Integer` |
| `long` | `Long` |
| `float` | `Float` |
| `double` | `Double` |
| `char` | `Character` |
| `boolean` | `Boolean` |

Wrapper classes matter because primitives are values, but wrappers are objects.

```java
Integer age = 12;
Double cost = 150250.55;
Boolean isActive = true;
```

## Why Wrappers Exist

Wrappers are useful for three main reasons:

- they provide methods and constants primitives do not have
- they allow primitive-like values to be used where objects are required
- they can be `null`

Example operations:

```java
int score = Integer.parseInt("8");
int max = Integer.MAX_VALUE;
boolean ok = Boolean.parseBoolean("true");
```

## Wrappers Can Be `null`

This is an important practical difference from primitives.

```java
int primitiveAge = 0;
Integer wrapperAge = null;
```

If `null` is meaningful in your model as "unknown" or "not set yet", wrappers can be useful. If you know a value must always exist, primitives are often simpler.

Warning: wrappers bring `null` into play, which means autounboxing can trigger `NullPointerException` if you are careless.

## Packages

Packages are Java's built-in way to organize related code.

You can think of a package like a namespace plus directory structure for:

- classes
- interfaces
- enums
- other related types

## Package Naming

Package names usually follow these conventions:

- all lowercase
- dot-separated segments
- user-defined packages often start with reversed domain ownership

Examples:

- `java.lang`
- `java.util`
- `java.math`
- `com.example.app`

## Imports

To use a type from another package, you typically import it near the top of the file.

```java
import java.math.BigInteger;
```

Or:

```java
import java.math.*;
```

Using the explicit class import is usually clearer when you only need one or two types.

## `java.lang` Is Special

Some base-language classes do not need explicit imports because `java.lang` is imported automatically.

This includes familiar types like:

- `String`
- `System`
- wrapper classes such as `Integer`
- `Exception`

That is why beginner Java code can use these types without adding `import` first.

## `java.math`

`java.math` is a good example of a package that exists because built-in numeric primitives are sometimes not enough.

Two important types are:

- `BigInteger` for very large integers
- `BigDecimal` for precise decimal arithmetic

```java
import java.math.BigDecimal;
import java.math.BigInteger;

BigInteger acct = new BigInteger("12345678901234567890");
BigDecimal price = new BigDecimal("19.99");
```

Common methods include:

- `.add(...)`
- `.subtract(...)`
- `.multiply(...)`
- `.divide(...)`

Key point: `BigDecimal` is especially important when decimal precision matters, such as money calculations.

## Interview Fast Answer

If someone asks what a POJO is, a strong short answer is:

- a simple Java object used mainly to store data
- usually has private fields with public getters and setters
- usually avoids framework-specific coupling and business logic

If the follow-up is about wrappers, the highest-signal answer is:

- wrappers let primitive-like values behave as objects
- they add methods/constants and allow `null`
- they are required in many generic collections

## Common Traps

- treating `String` like a primitive because it appears early in beginner code
- forgetting that wrapper types can be `null`
- assuming getters/setters are pointless because they only forward fields today
- using wildcard imports everywhere when a smaller import list would be clearer
- using floating-point primitives where exact decimal arithmetic is required

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
