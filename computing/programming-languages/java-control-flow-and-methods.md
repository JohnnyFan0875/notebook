# Java Control Flow and Methods

After basic syntax and variables, the next big Java step is learning how to:

- group logic into reusable methods
- choose behavior with conditions
- repeat behavior with loops

This note stays at that level: practical control flow, not full object-oriented design.

## What a Method Is

A method is a named block of code that performs a task.

Why methods matter:

- they reduce repetition
- they make intent easier to read
- they let you reuse behavior from multiple places

At a high level, a method has:

- a return type
- a method name
- optional parameters
- a body

```java
returnType methodName() {
    // code
}
```

## `void` vs Returning a Value

Some methods only do an action:

```java
void sayHello() {
    System.out.println("Hello");
}
```

`void` means the method does not return a value.

Other methods compute and return something:

```java
int squareNumber(int number) {
    return number * number;
}
```

Key point: if the return type is not `void`, the method should produce a matching `return` value.

## Parameters

Parameters let a method work with input values instead of hard-coded data.

```java
void sayHello(String name) {
    System.out.println("Hello " + name);
}
```

Methods can take multiple parameters and mixed types:

```java
void printUser(String name, int age, String address) {
    System.out.println(name + " is " + age + " and lives at " + address);
}
```

Useful intuition:

- parameters are the inputs
- the return value is the output

## Calling Methods

Defining a method does nothing by itself. The method must be called.

```java
public static void main(String[] args) {
    sayHello("Maria");
    int squared = squareNumber(5);
    System.out.println(squared);
}
```

This is one of the easiest beginner misses: writing a method correctly but forgetting to invoke it.

## `if` Statements

Control flow decides what code runs based on conditions.

The simplest conditional form is:

```java
if (score >= 90) {
    System.out.println("Great job!");
}
```

If the condition is `true`, the block runs. If it is `false`, Java skips it.

## `if` / `else if` / `else`

Use chained conditionals when several mutually exclusive paths are possible.

```java
if (score >= 90) {
    System.out.println("Excellent!");
} else if (score >= 70) {
    System.out.println("Good effort.");
} else {
    System.out.println("Keep trying!");
}
```

Key point: once one branch matches, the later branches do not run.

## Logical Operators in Conditions

Conditions often combine smaller boolean checks.

```java
if (score > 80 && isAttending) {
    System.out.println("Eligible");
}
```

The most common operators are:

| Operator | Meaning |
| -------- | ------- |
| `&&` | and |
| `||` | or |
| `!` | not |

These make conditional logic more expressive, but overly dense conditions can become hard to read.

## `switch`

`switch` is useful when many branches depend on one expression value.

```java
switch (direction) {
    case 'N':
        System.out.println("North");
        break;
    case 'S':
        System.out.println("South");
        break;
    default:
        System.out.println("Unknown");
}
```

It often reads more cleanly than a long chain of equality-based `if` checks.

## Why `break` Matters in `switch`

Without `break`, execution falls through into later cases.

```java
switch (direction) {
    case 'N':
        System.out.println("North");
    case 'S':
        System.out.println("South");
}
```

If `direction` is `'N'`, both lines run here.

That can be intentional, but most beginner switch bugs come from forgetting `break`.

## `for` Loops

Use a `for` loop when the repetition pattern is known up front.

```java
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}
```

The three parts mean:

- initialize the loop variable
- continue while the condition stays true
- update the loop variable after each iteration

This is the usual default loop when counting or walking array indexes.

## Looping Through Arrays

```java
String[] names = {"Ana", "Ben", "Cara"};

for (int i = 0; i < names.length; i++) {
    System.out.println(names[i]);
}
```

This style is useful when you need the index as well as the value.

## Enhanced `for` Loop

When you only need each element and not its position, the enhanced loop is simpler.

```java
for (String name : names) {
    System.out.println(name);
}
```

It improves readability, but it is less suitable when index-based logic matters.

## `while` Loops

Use a `while` loop when you do not know in advance how many times the loop should run.

```java
int counter = 0;

while (counter < 3) {
    System.out.println(counter);
    counter++;
}
```

This pattern keeps running while the condition remains true.

## Infinite Loops

The most common `while` bug is forgetting to change the state that the condition depends on.

```java
int counter = 0;

while (counter < 3) {
    System.out.println(counter);
}
```

This loop never updates `counter`, so it never finishes.

A useful mental check is:

- what makes the condition become false?

If the answer is unclear, the loop may be unsafe.

## `break`

`break` exits the current loop early.

```java
for (int i = 0; i < 10; i++) {
    if (i == 2) {
        break;
    }
    System.out.println(i);
}
```

This prints `0` and `1`, then stops the loop.

`break` is sometimes the right tool, but if it appears everywhere, the loop structure may need simplification.

## Putting It Together

Small Java programs often combine methods with control flow:

```java
static boolean isEven(int n) {
    return (n % 2) == 0;
}

public static void main(String[] args) {
    int number = 2345;

    if (isEven(number)) {
        System.out.println("Even");
    } else {
        System.out.println("Odd");
    }
}
```

This is a good pattern to internalize:

- keep reusable logic in methods
- keep high-level decisions in the calling flow

## Common Traps

- forgetting to call a method after defining it
- using a non-`void` return type without returning a value
- writing long condition chains that hide the real decision logic
- forgetting `break` in `switch`
- off-by-one errors in `for` loop bounds
- creating `while` loops that never change the controlling state
- using an index loop when an enhanced `for` loop would be clearer

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java OOP](java-oop.md)
- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
