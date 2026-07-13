# Java Testing

Testing in Java is usually introduced through `JUnit`, then expanded into broader ideas like edge cases, integration tests, and mocks.

This note keeps the focus on practical test-writing habits rather than framework trivia.

## What Testing Is For

Software testing checks whether code behaves as expected under both normal and unusual conditions.

Two recurring ideas matter early:

- verify expected behavior
- probe edge cases and failure paths

If the code only works on the happy path, it is usually not tested enough.

## Edge Cases

An edge case is an input or condition near the boundary of what the program normally expects.

Common examples:

- `null`
- empty strings or empty collections
- negative values
- maximum or minimum numeric values
- values just inside or outside a validation rule

Good tests deliberately include these cases instead of treating them as afterthoughts.

## `JUnit 5`

`JUnit 5` is the standard beginner-friendly testing library in modern Java.

A minimal test looks like this:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CalculatorTest {
    @Test
    void add_returnsSum() {
        int actual = 2 + 2;
        assertEquals(4, actual);
    }
}
```

`@Test` marks a method as a test case.

## Arrange, Act, Assert

A useful structure for most tests is:

- arrange inputs and setup
- act by calling the code under test
- assert the expected outcome

```java
@Test
void add_returnsSum() {
    // Arrange
    int left = 2;
    int right = 2;

    // Act
    int actual = left + right;

    // Assert
    assertEquals(4, actual);
}
```

This pattern keeps tests readable and reduces hidden setup.

## Core Assertions

Some of the most common JUnit assertions are:

- `assertEquals(expected, actual)`
- `assertTrue(condition)`
- `assertFalse(condition)`
- `assertNull(value)`
- `assertNotNull(value)`

One easy mistake is swapping argument order in `assertEquals`. JUnit expects `expected` first and `actual` second.

## Asserting Exceptions

Exception behavior is often part of the contract and should be tested directly.

```java
import static org.junit.jupiter.api.Assertions.assertThrows;

@Test
void parse_throwsOnBadInput() {
    assertThrows(NumberFormatException.class, () -> Integer.parseInt("abc"));
}
```

If a method is supposed to reject invalid input, that rejection belongs in the test suite.

## Naming Tests

A project can easily contain hundreds of tests, so names should explain intent quickly.

A practical naming style is:

- `method_condition_expectedResult`

Examples:

- `isValidUsername_null_returnsFalse`
- `convertEuroTo_mockedRate_returnsExpectedAmount`

Good test names reduce the need to inspect the method body when a failure appears in CI output.

## Unit Tests vs Integration Tests

These two categories answer different questions.

| Unit tests | Integration tests |
| ---------- | ----------------- |
| test one component in isolation | test how multiple components work together |
| failures are easier to localize | failures take more tracing |
| usually faster | usually heavier and slower |
| often avoid real dependencies | often involve real dependencies |

Key point: unit tests optimize for precision and speed, while integration tests optimize for realism.

## Dependencies and Why They Matter

A dependency is another component your code relies on.

Examples:

- an API client
- a database layer
- a file store
- a service object from another module

Testing gets harder when the dependency is slow, nondeterministic, or not under your control.

## Mocking with Mockito

When a dependency should not be exercised for real in a unit test, mocking is a common approach.

`Mockito` is a widely used Java mocking library.

```java
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

EuropeanCentralBankServer bank = mock(EuropeanCentralBankServer.class);
when(bank.getRateEuroTo("JPY")).thenReturn(110.0);
```

This creates a fake dependency and programs a chosen response.

That programming step is called stubbing.

## Why Mocking Helps

Mocks help when you want to:

- isolate the code under test
- avoid network or database calls
- make results deterministic
- assert exact outcomes instead of loose sanity checks

Without stubbing, a mock often returns Java defaults like `0`, `false`, or `null`, which can make tests fail for confusing reasons.

## Verifying Mock Usage

Sometimes the important question is not just what value came back, but whether a dependency was called.

```java
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

verify(infoStore).save("ok");
verifyNoInteractions(errorStore);
```

Use this when interaction behavior is part of the requirement.

## Parameterized Tests

Parameterized tests reduce duplication when the same logic should be checked with many inputs.

Instead of writing many nearly identical `@Test` methods, you write one test and feed it multiple cases.

## `@ValueSource`

Use `@ValueSource` when each case supplies a single primitive-like value.

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

@ParameterizedTest
@ValueSource(strings = {"", "jane doe"})
void isValidUsername_invalidInputs_returnFalse(String username) {
    assertFalse(isValidUsername(username));
}
```

Useful point: the attribute name is plural, such as `strings`, `ints`, or `booleans`.

## `@NullSource`

`@ValueSource` cannot include `null`.

Use `@NullSource` when `null` should be one of the cases:

```java
import org.junit.jupiter.params.provider.NullSource;

@ParameterizedTest
@NullSource
@ValueSource(strings = {"", "jane doe"})
void isValidUsername_invalidInputs_returnFalse(String username) {
    assertFalse(isValidUsername(username));
}
```

This is a clean way to include a classic edge case without duplicating the test body.

## `@CsvSource`

When each test case needs multiple values, `@CsvSource` is often the simplest option.

```java
import org.junit.jupiter.params.provider.CsvSource;

@ParameterizedTest
@CsvSource({
    "Hello World, 11",
    "DataCamp, 8",
    "'', 0"
})
void length_returnsExpectedValue(String text, int expected) {
    assertEquals(expected, text.length());
}
```

This works well for compact tables of input/output examples.

## `@MethodSource`

If the inputs are more complex objects, `@MethodSource` is usually the flexible choice.

```java
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

@ParameterizedTest
@MethodSource("provideNames")
void fullName_returnsExpectedValue(Person person, String expected) {
    assertEquals(expected, person.fullName(person));
}
```

The provider method returns argument sets:

```java
private static List<Arguments> provideNames() {
    return List.of(
        Arguments.of(new Person("John", "Doe"), "John Doe"),
        Arguments.of(new Person("Jane", "Doe"), "Jane Doe")
    );
}
```

Use this when the data is too rich for `@ValueSource` or `@CsvSource`.

## When to Prefer Each Parameter Source

- use `@ValueSource` for one simple input value
- use `@NullSource` when `null` must be included
- use `@CsvSource` for small multi-column examples
- use `@MethodSource` for objects or more expressive setup

## Common Traps

- testing only happy paths and skipping edge cases
- reversing `expected` and `actual` in `assertEquals`
- writing integration tests when a fast unit test would do
- using mocks without stubbing their behavior
- overusing parameterized tests when the cases are too different to stay readable
- forcing complex object cases into `@ValueSource`

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
- [Java File I/O and Streams](java-file-io-and-streams.md)
