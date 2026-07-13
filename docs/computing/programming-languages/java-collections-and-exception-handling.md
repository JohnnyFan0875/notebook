# Java Collections and Exception Handling

After arrays and basic objects, Java programming quickly becomes about two recurring problems:

- how to manage groups of objects
- how to deal with failure without losing control flow

This note groups those two areas because they show up together in ordinary application code very quickly.

## Collections Framework

The Java Collections Framework is a built-in set of reusable data-structure types, mostly centered in `java.util`.

Its purpose is to avoid rebuilding common containers from scratch and to give a shared vocabulary for storing and manipulating groups of objects.

## Arrays vs Collections

Arrays and collections overlap, but they are not interchangeable.

| Arrays | Collections |
| ------ | ----------- |
| fixed length | dynamically resizable in many implementations |
| can store primitives directly | usually store objects |
| minimal built-in behavior | richer built-in operations |
| good for fixed-size, simple storage | better for growth, lookup, reordering, and abstraction |

Key point: arrays are still useful, but when you need flexible size or higher-level operations, collections are often the better default.

## Two Big Families

The framework is commonly introduced through two top-level ideas:

| Family | Purpose |
| ------ | ------- |
| `Collection` | store groups of objects |
| `Map` | store key-value associations |

Inside `Collection`, the most important interfaces for beginners are:

- `List`
- `Set`
- `Queue`

## Generics

Collections are usually parameterized with generics.

```java
ArrayList<String> animals = new ArrayList<String>();
```

The type parameter tells Java what kind of objects the collection should hold.

Why generics matter:

- better type safety
- fewer casts
- clearer intent

Without generics, a collection can become a mixed bag of `Object`, which is legal but much less safe.

## `List`

`List` is for ordered collections that can contain duplicates.

Two common implementations are:

- `ArrayList`
- `LinkedList`

### `ArrayList`

`ArrayList` is the usual default choice.

```java
import java.util.ArrayList;

ArrayList<String> animals = new ArrayList<String>();
animals.add("horse");
animals.add("cow");
animals.add("chicken");

String first = animals.get(0);
animals.set(1, "goat");
```

Useful operations:

- `.add(...)`
- `.get(index)`
- `.set(index, value)`
- `.remove(index or value)`

### `LinkedList`

`LinkedList` supports the same `List` interface, but with a different internal structure.

```java
import java.util.LinkedList;

LinkedList<String> cars = new LinkedList<String>();
cars.addFirst("Fiat");
cars.addLast("BMW");
```

Useful when:

- you frequently add/remove near the ends or middle

Less ideal when:

- you do lots of random index access

### `ArrayList` vs `LinkedList`

Good beginner rule of thumb:

- choose `ArrayList` by default
- switch to `LinkedList` only when your mutation pattern clearly benefits

## Autoboxing

Collections usually work with objects, not primitives, so wrappers matter here.

```java
ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(5);
```

`5` is automatically boxed into `Integer`.

Key point: this automatic primitive-to-wrapper conversion is called autoboxing.

## `Set`

`Set` is for uniqueness.

```java
import java.util.HashSet;

HashSet<String> words = new HashSet<String>();
words.add("java");
words.add("java");
words.add("jvm");
```

The duplicate `"java"` is ignored.

Good when:

- membership testing matters
- duplicates should not exist

Less suitable when:

- ordering or index-based access is important

## `Queue`

`Queue` models first-in, first-out processing.

```java
import java.util.concurrent.ArrayBlockingQueue;

ArrayBlockingQueue<String> queue = new ArrayBlockingQueue<String>(4);
queue.offer("A");
queue.offer("B");
String next = queue.poll();
```

Useful distinctions:

- `.add(...)` may throw if capacity is exceeded
- `.offer(...)` returns failure instead of throwing in that situation
- `.remove()` may throw on empty queue
- `.poll()` returns `null` on empty queue

## `Map`

`Map` stores associations from keys to values.

```java
import java.util.HashMap;

HashMap<Integer, String> users = new HashMap<Integer, String>();
users.put(101, "Alice");
users.put(102, "Bob");

String name = users.get(101);
```

Core operations:

- `.put(key, value)`
- `.get(key)`
- `.remove(key)`

Use a map when lookup by key is the real job, not ordered sequence handling.

## Supporting Utility Classes

Two useful helper classes are:

- `java.util.Collections`
- `java.util.Arrays`

Examples:

```java
Collections.sort(list);
Collections.reverse(list);

List<String> countries = Arrays.asList(arrayCountries);
```

`Collections` helps manipulate collection instances. `Arrays` helps bridge array-oriented operations.

## Exceptions

In Java, exceptions represent problems that interrupt normal control flow.

Common sources:

- wrong input
- coding mistakes
- unexpected runtime conditions

Java throws exceptions to signal that the normal path could not continue as written.

## `try` / `catch`

The basic recovery structure is:

```java
try {
    String x = list.get(3);
} catch (IndexOutOfBoundsException e) {
    System.out.println("Oops - wrong index");
}
```

The idea is:

- `try` runs risky code
- `catch` handles a matching exception type

## Multiple `catch` Blocks

You can handle different exception types differently.

```java
try {
    // risky code
} catch (IndexOutOfBoundsException eIndex) {
    System.out.println("Bad index");
} catch (NumberFormatException eValue) {
    System.out.println("Bad number");
}
```

Java checks the `catch` blocks in order until it finds a match.

## `finally`

`finally` is for cleanup code that should run whether an exception happened or not.

```java
try {
    Integer.valueOf("one");
} catch (NumberFormatException e) {
    System.out.println("Oops");
} finally {
    System.out.println("Doing cleanup");
}
```

## Exception Objects Carry Information

The caught exception object is not just a signal; it also contains context.

Useful methods:

- `.getMessage()`
- `.getClass()`

The stack trace gives execution-path context for where the problem happened.

## Exceptions vs Errors

Java distinguishes between exceptions and more serious errors.

| Kind | Typical meaning |
| ---- | --------------- |
| Exception | something the application may handle or recover from |
| Error | serious problem the application usually does not handle |

For example, `OutOfMemoryError` is not the kind of issue you normally recover from with ordinary control-flow logic.

## Checked vs Unchecked Exceptions

This distinction is central in Java.

| Type | Meaning |
| ---- | ------- |
| Checked exception | must be handled or declared |
| Unchecked exception | subtype of `RuntimeException`; handling is optional |

Rough mental model:

- checked exceptions often represent conditions outside your direct control
- unchecked exceptions often reflect programming mistakes or bad assumptions

Common runtime examples:

- `ArithmeticException`
- `IndexOutOfBoundsException`
- `NegativeArraySizeException`
- `NullPointerException`
- `NumberFormatException`

## `throws`

Instead of handling an exception locally, a method can declare that it passes responsibility upward.

```java
public static void loadThing() throws ClassNotFoundException {
    Class<?> myClass = Class.forName("com.mysql.Driver");
}
```

This is often described as "passing the buck".

Key point: `throws` is sometimes necessary, but local handling with `try/catch` is usually clearer when the method actually knows how to recover.

## Rethrowing

You can catch an exception and then throw it again.

This is useful when:

- you want to add context
- you can only partially handle the issue
- a higher layer should decide the final response

## Logging

Logging is the structured cousin of `System.out.println(...)`.

Java includes built-in logging support.

```java
import java.util.logging.Level;
import java.util.logging.Logger;

Logger logger = Logger.getLogger("MyClass");
logger.log(Level.INFO, "This is informational");
logger.log(Level.SEVERE, "This is critical");
```

Why logging matters:

- records what happened
- helps debug control flow
- gives production-friendly diagnostics

Typical levels include:

- `SEVERE`
- `WARNING`
- `INFO`
- `CONFIG`
- `FINE`

## Interview Fast Answer

If someone asks for the practical difference between `List`, `Set`, and `Map`, a good short answer is:

- `List`: ordered, allows duplicates
- `Set`: unique elements, usually no index-based access
- `Map`: key-value lookup table

If the follow-up is about exceptions, the highest-signal answer is:

- checked exceptions must be handled or declared
- unchecked exceptions are usually programming mistakes and do not require explicit handling
- `try/catch/finally` controls local recovery and cleanup

## Common Traps

- using raw collections without generics
- reaching for `LinkedList` by default when `ArrayList` would be simpler
- forgetting that collections usually work with objects, not primitives
- confusing `.add()` and `.offer()` style behavior on queues
- catching overly broad `Exception` too early and hiding useful detail
- overusing `throws` when local handling would be clearer
- relying on `System.out.println(...)` where logging is the better long-term tool

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Objects and Packages](java-objects-and-packages.md)
