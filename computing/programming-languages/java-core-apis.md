# Java Core APIs

This note collects a few high-frequency Java standard-library areas that are useful early, but do not fit neatly into syntax, OOP, or collections alone.

## Date and Time with `java.time`

Modern Java date/time work usually starts with `java.time`.

Two especially common types are:

| Type | Purpose |
| ---- | ------- |
| `LocalDate` | date without time |
| `LocalTime` | time without date |

```java
import java.time.LocalDate;
import java.time.LocalTime;

LocalDate date = LocalDate.now();
LocalTime time = LocalTime.now();
```

Key point: `LocalDate` and `LocalTime` intentionally separate concepts that older date APIs often mixed together awkwardly.

## Formatting Dates

`DateTimeFormatter` controls how dates are rendered or parsed.

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

LocalDate date = LocalDate.now();
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy");
String formatted = date.format(formatter);
```

This is useful whenever the default ISO format is not what the application or user interface expects.

## Parsing Dates from Strings

```java
LocalDate parsedDate = LocalDate.parse("2024-03-10");
```

Parsing works only when the text matches the expected format.

If the input uses a custom format, you typically provide a matching formatter.

## Date Adjustment

```java
LocalDate date = LocalDate.now();
LocalDate futureDate = date.plusDays(7);
LocalDate pastDate = date.minusDays(7);
```

These methods make common calendar arithmetic much easier to read than manual numeric manipulation.

## Enums

Enums define a fixed set of allowed values.

```java
enum Day {
    MONDAY,
    TUESDAY,
    WEDNESDAY
}
```

They are useful when:

- the value should come from a controlled closed set
- readability matters more than magic strings or arbitrary integers

## Why Enums Help

Enums improve code quality by:

- preventing invalid values
- making intent explicit
- keeping related named constants together

Typical examples:

- days of the week
- order status
- workflow states

## Using Enums

```java
Day today = Day.WEDNESDAY;
System.out.println(today);
```

You can also iterate across the declared values:

```java
for (Day day : Day.values()) {
    System.out.println(day + " -> " + day.ordinal());
}
```

`ordinal()` gives the declared position, but it is usually better treated as metadata than as stable business meaning.

## Enums with Data and Methods

Enums can contain fields, constructors, and methods.

```java
enum Status {
    SUCCESS("Operation successful"),
    ERROR("An error occurred");

    private final String message;

    Status(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
```

This is useful when each enum constant needs attached behavior or descriptive metadata.

## Recursion

Recursion means a method solves a problem by calling itself on a smaller version of that problem.

```java
static void countdown(int n) {
    if (n == 0) {
        return;
    }
    System.out.println(n);
    countdown(n - 1);
}
```

The key requirement is a base case that stops the chain.

Without that stop condition, recursion never bottoms out.

## When Recursion Is a Good Fit

Recursion is most natural when:

- the problem is structurally self-similar
- each step reduces to a smaller subproblem
- the base case is simple and clear

It is often more elegant than loops for trees, divide-and-conquer logic, or explicitly recursive definitions.

## Interview Fast Answer

If someone asks why use `LocalDate` instead of raw strings, a strong short answer is:

- it gives type safety
- built-in parsing/formatting
- safe date arithmetic like `.plusDays()` and `.minusDays()`

If the follow-up asks why use enums, the high-signal answer is:

- enums model a fixed valid set of states
- they improve readability and prevent invalid ad hoc values
- they can also carry fields and methods when needed

## Common Traps

- treating date strings as if they were already structured date values
- assuming parsing will work when the string format does not match
- using `ordinal()` as durable business logic
- using plain strings where an enum would better constrain valid states
- writing recursion without a clear base case

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java OOP](java-oop.md)
