# Java Fundamentals

Java is a general-purpose, statically typed language with a steeper learning curve than Python or JavaScript, but that strictness is also part of why Java scales well for larger codebases. For notebook purposes, the important thing is not memorizing every keyword, but understanding the small set of structural rules that Java expects from the start.

## Core Mental Model

If you are new to Java, three ideas explain most of the "why is this so formal?" feeling:

- code lives inside classes
- variables always have declared types
- syntax is explicit about boundaries and intent

That means Java often feels more verbose at first, but it also makes program structure easier to reason about once the conventions are familiar.

## Minimal Program Structure

The most common beginner shape is:

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```

Key pieces:

- `class` groups related code
- `main` is the entry point for a runnable program
- `System.out.println(...)` prints a value and moves to a new line

## Syntax Rules That Matter Early

Java is case-sensitive and relatively strict about punctuation.

```java
public class Main {
    public static void main(String[] args) {
        int age = 29;
        System.out.println(age);
    }
}
```

Early habits worth locking in:

- `Main` and `main` are different identifiers
- statements usually end with `;`
- whitespace helps readability, but does not replace required syntax
- `=` is assignment, not equality checking

## Variables

Java variables have three parts:

```java
type variableName = value;
```

Examples:

```java
String message = "Java is awesome!";
int age = 29;
boolean isActive = true;
```

Good beginner heuristics:

- pick names that describe meaning, not storage
- use `camelCase` for variable names
- remember that the declared type constrains what values the variable can hold

## Primitive Types

Java primitives are the built-in value types that are not objects.

### Whole numbers

| Type | Typical use |
| ---- | ----------- |
| `int` | default choice for whole numbers |
| `long` | larger whole-number range |
| `short` | smaller-range integers, uncommon in everyday code |
| `byte` | very small integer range, often low-level or compact storage use |

Most of the time, `int` is the right first choice unless you specifically need a different range.

### Decimal numbers

| Type | Typical use |
| ---- | ----------- |
| `double` | default choice for decimal values |
| `float` | lower precision decimal type |

In ordinary Java application code, `double` is usually the primitive of choice for decimals.

### Other common primitives

| Type | Meaning |
| ---- | ------- |
| `boolean` | `true` or `false` |
| `char` | one single character in single quotes |

Examples:

```java
boolean isPaid = false;
char initial = 'J';
```

## `char` vs `String`

This distinction matters early because the syntax looks similar but the meaning is not.

```java
char initial = 'J';
String name = "Jim";
```

- `char` stores one character and uses single quotes
- `String` stores a sequence of characters and uses double quotes

Key point: a single character inside double quotes is still a `String`, not a `char`.

## Strings

Strings are not primitives, but they are used constantly and are usually learned alongside them.

```java
String userName = "JSmith13";
int userNameLength = userName.length();
String lower = userName.toLowerCase();
String upper = userName.toUpperCase();
```

Common beginner-useful operations:

- `.length()` returns the number of characters as an `int`
- `.toLowerCase()` and `.toUpperCase()` change case
- `+` concatenates strings

```java
String message1 = "Java is";
String message2 = "awesome";
String fullMessage = message1 + " " + message2;
```

If one side of `+` is a `String`, Java will coerce the other side into string form during concatenation.

## Arrays

Arrays store multiple values of the same type under one variable.

```java
int[] prices = {10, 20, 30, 40};
```

Useful early rules:

- arrays are zero-indexed
- array length is fixed once created
- access uses square brackets

```java
int first = prices[0];
prices[2] = 95;
int n = prices.length;
```

Key point: `prices.length` is a property on the array, while `someString.length()` is a method on `String`.

## Arithmetic Operators

Java includes the usual arithmetic operators:

| Operator | Meaning |
| -------- | ------- |
| `+` | addition |
| `-` | subtraction |
| `*` | multiplication |
| `/` | division |
| `++` | increment by 1 |
| `--` | decrement by 1 |

Example:

```java
int a = 5 + 6;
a++;
```

### Integer division

This is one of the most common beginner surprises.

```java
int numOrders = 100;
int days = 30;
int avgOrders = numOrders / days;
```

Here the result is `3`, not `3.333...`, because dividing two integers produces integer division.

If you need a decimal result, at least one side must be treated as decimal:

```java
double avgOrders = (double) numOrders / days;
```

## Comparison Operators

Comparison operators evaluate to `boolean`.

| Operator | Meaning |
| -------- | ------- |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `==` | equal to |
| `!=` | not equal to |

Example:

```java
int minSpend = 25;
int total = 23;
boolean paidDelivery = total <= minSpend;
```

Warning: `=` assigns a value. `==` compares values. Mixing them up is one of the most common early syntax and logic errors.

## Interview Fast Answer

If someone asks what feels different about Java compared with more dynamic beginner languages, a good short answer is:

- Java is statically typed, so variables need declared types
- runnable code is usually structured through classes and a `main` method
- syntax is stricter, but that explicitness helps with maintainability

If the follow-up is about beginner essentials, the highest-signal topics are:

- primitives vs `String`
- integer division
- `char` vs `String`
- `=` vs `==`
- array indexing and fixed length

## Common Beginner Traps

- forgetting that Java is case-sensitive
- using `=` when you meant `==`
- expecting integer division to produce decimals
- treating `char` and `String` as interchangeable
- trying to access an array index beyond its fixed length
- assuming `System.out.println(array)` prints array contents nicely

## Related Notes

- [Computer Science Foundations](../computer-science-foundations/README.md)
- [Programming Paradigms](../computer-science-foundations/programming-paradigms.md)
